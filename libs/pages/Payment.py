import random
import os
import time
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from selenium.common.exceptions import ElementClickInterceptedException


class Payment:
    class Paymentlocators:
        PAYMENT_HEADER="//h2[@class='heading']"
        NAME_ON_CARD_SLOT="//input[@name='name_on_card']"
        CARD_NUMBER_SLOT="//input[@name='card_number']"
        CVC_NUMBER_SLOT="//input[@placeholder='ex. 311']"
        EXPRIRATION_MONTH="//input[@placeholder='MM']"
        EXPIRATION_YEAR="//input[@placeholder='YYYY']"
        PAY_AND_CONFIRM_ORDER="//button[@id='submit']"
        ORDER_PLACED_NOTIFICATION="//b[normalize-space()='Order Placed!']"
        DOWNLOAD_INVOICE_BUTTON="//a[@class='btn btn-default check_out']"
        CONTINUE_BUTTON="//a[@class='btn btn-primary']"
        MAIN_LOGO="//img[@alt='Website for automation practice']"
    
    def __init__(self):
        """Määrittää Selenium-kirjaston käytettäväksi myöhempää varten"""
        try:
            self.selib = BuiltIn().get_library_instance("SeleniumLibrary")
        except RobotNotRunningError:
            self.selib = None
        
        # Oletusarvot asetetaan tässä. ÄLÄ lue Robot-muuttujia __init__:ssä.
        self.base_url = "https://automationexercise.com/"
        self.default_browser = "chrome"

    def _selib(self):
        """Ottaa Selenium-kirjaston käyttöön"""
        if not self.selib:
            self.selib = BuiltIn().get_library_instance("SeleniumLibrary")
        return self.selib

    def __getattr__(self, name):
        return getattr(self._selib(), name)
    
    @staticmethod
    def get_randomnumbers(length):
        numbers = [0,1,2,3,4,5,6,7,8,9]
        random_numbers_list = random.choices(numbers, k=length)
        return "".join(str(num) for num in random_numbers_list)
    
    @staticmethod
    def get_randommonth():
        months=[1,2,3,4,5,6,7,8,9,10,11,12]
        random_month = random.choice(months)
        return random_month
    
    @staticmethod
    def get_randomyear():
        years=[2026, 2027, 2028, 2029]
        random_year = random.choice(years)
        return random_year
    
    def _safe_click(self, loc):
        """
        Yrittää klikata elementtiä kolmella tavalla:
        1) Normaali Selenium-klikkaus
        2) Piilota mainos-iframet ja yritä uudelleen
        3) Suora JavaScript click
        Palauttaa True/False onnistumisen mukaan.
        """
        # 1 — Normaali klikkaus
        try:
            self.selib.click_element(loc)
            return True
        except ElementClickInterceptedException:
            pass
        except Exception:
            pass

        # 2 — Piilota mainos-iframet
        js_hide_ads = """
            document.querySelectorAll("iframe[id^='aswift'], iframe[title='Advertisement']")
                    .forEach(el => el.style.display = 'none');
        """
        try:
            self.selib.execute_javascript(js_hide_ads)
            self.selib.sleep(0.3)
        except Exception:
            pass

        # Yritä uudelleen
        try:
            self.selib.click_element(loc)
            return True
        except Exception:
            pass

        # 3 — JS fallback - klikkaus
        try:
            we = self.selib.find_element(loc)
            self.selib.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", we)
            self.selib.driver.execute_script("arguments[0].click();", we)
            return True
        except Exception:
            return False

    
    @keyword
    def pay_order(self, USERNAME):
        """
        Täyttää maksutiedot, arpoo kortin numeron, cvc:n sekä kuukausi/vuosi
        ja suorittaa turvallisen klikkauksen (mainoksen ohi).
        """
        card_number = self.get_randomnumbers(20)
        cvc_number = self.get_randomnumbers(3)
        month = self.get_randommonth()
        year = self.get_randomyear()

        self.selib.input_text(self.Paymentlocators.NAME_ON_CARD_SLOT, USERNAME)
        self.selib.input_text(self.Paymentlocators.CARD_NUMBER_SLOT, card_number)
        self.selib.input_text(self.Paymentlocators.CVC_NUMBER_SLOT, cvc_number)
        self.selib.input_text(self.Paymentlocators.EXPRIRATION_MONTH, month)
        self.selib.input_text(self.Paymentlocators.EXPIRATION_YEAR, year)

        self._safe_click(self.Paymentlocators.PAY_AND_CONFIRM_ORDER)

        self.wait_until_element_is_visible(self.Paymentlocators.ORDER_PLACED_NOTIFICATION, timeout='5s')

    @keyword
    def download_invoice(self):
        self.wait_until_element_is_visible(self.Paymentlocators.ORDER_PLACED_NOTIFICATION, timeout='5s')
        self.click_element(self.Paymentlocators.DOWNLOAD_INVOICE_BUTTON)
        
    @keyword
    def verify_invoice_exists(self, timeout=30):
        """
        Odottaa, että Downloads-kansioon ilmestyy tiedosto, jonka nimessä esiintyy 'invoice'.
        Palauttaa True jos löytyy, muuten epäonnistuu (AssertionError).
        """
        downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(downloads):
            raise AssertionError(f"Downloads-kansiota ei löydy: {downloads}")

        end_time = time.time() + int(timeout)
        while time.time() < end_time:
            for file in os.listdir(downloads):
                if "invoice" in file.lower():
                    return True
            time.sleep(1)
        raise AssertionError(f"No invoice file found in {downloads} after {timeout} seconds.")

    @keyword
    def go_to_main_page(self):
        self.wait_until_element_is_visible(self.Paymentlocators.ORDER_PLACED_NOTIFICATION, timeout='5s')
        self.click_element(self.Paymentlocators.CONTINUE_BUTTON)
        self.wait_until_element_is_visible(self.Paymentlocators.MAIN_LOGO, timeout='5s')



