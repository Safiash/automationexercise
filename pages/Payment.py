import random
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from selenium.common.exceptions import ElementClickInterceptedException


class Payment:
    class Paymentlocators:
        PAYMENT="//h2[@class='heading']"
        NAME_ON_CARD_SLOT="//input[@name='name_on_card']"
        CARD_NUMBER_SLOT="//input[@name='card_number']"
        CVC="//input[@placeholder='ex. 311']"
        EXPRIRATION_MONTH="//input[@placeholder='MM']"
        EXPIRATION_YEAR="//input[@placeholder='YYYY']"
        PAY_AND_CONFIRM_ORDER="//button[@id='submit']"
        ORDER_PLACED="//b[normalize-space()='Order Placed!']"
        CONTINUE="//a[@class='btn btn-primary']"
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
    
    @keyword
    def pay_order(self, USERNAME):
        """
        Täyttää maksutiedot, ottaa nimen usernamesta, arpoo 20 random lukua kortin numeroksi ja 3 random lukua cvc luvuksi ja arpoo
        sitten random kuukauden ja vuoden. lopuksi vahvistaa tilauksen. 
        """
        card_number = self.get_randomnumbers(20)
        self.selib.input_text(self.Paymentlocators.NAME_ON_CARD_SLOT, USERNAME)
        self.input_text(self.Paymentlocators.CARD_NUMBER_SLOT, card_number)
        cvc_number = self.get_randomnumbers(3)
        self.selib.input_text(self.Paymentlocators.CVC, cvc_number)
        month = self.get_randommonth()
        self.selib.input_text(self.Paymentlocators.EXPRIRATION_MONTH, month)
        year = self.get_randomyear()
        self.selib.input_text(self.Paymentlocators.EXPIRATION_YEAR, year)

        # ---- KIERRÄ MAINOS (iframe-piilotus) ----
        js_hide_ads = """
            document.querySelectorAll("iframe[id^='aswift'], iframe[title='Advertisement']")
                    .forEach(el => el.style.display = 'none');
        """
        try:
            self.selib.execute_javascript(js_hide_ads)
            self.selib.sleep(0.3)  # pieni viive että DOM päivittyy
        except Exception:
            pass
        # -----------------------------------------

        try:
            self.click_element(self.Paymentlocators.PAY_AND_CONFIRM_ORDER)
        except ElementClickInterceptedException:
            # Jos edelleen jää mainoksen alle, käytetään suoraa JS-klikkausta
            try:
                we = self.selib.find_element(self.Paymentlocators.PAY_AND_CONFIRM_ORDER)
                self.selib.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", we)
                self.selib.driver.execute_script("arguments[0].click();", we)
            except Exception:
                raise AssertionError("PAY_AND_CONFIRM_ORDER element could not be clicked even after hiding ads.")

        self.wait_until_element_is_visible(self.Paymentlocators.ORDER_PLACED, timeout='5s')
        self.click_element(self.Paymentlocators.CONTINUE)
        self.wait_until_element_is_visible(self.Paymentlocators.MAIN_LOGO, timeout='5s')






