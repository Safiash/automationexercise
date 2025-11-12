import random
import string
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from selenium.common.exceptions import ElementClickInterceptedException


class SignLogin:

    class SignLoginLocators:
        LOGIN_YOUR_ACCOUNT_TEXT = "//h2[normalize-space()='Login to your account']"
        LOGIN_EMAIL = "//input[@data-qa='login-email']"
        LOGIN_PASSWORD = "//input[@placeholder='Password']"
        LOGIN_BUTTON = "//button[normalize-space()='Login']"

        SIGN_UP_NAME = "//input[@placeholder='Name']"
        SIGN_UP_EMAIL = "//input[@data-qa='signup-email']"
        SIGN_UP_BUTTON = "//button[normalize-space()='Signup']"
        #account_information
        HEADER = "//b[normalize-space()='Enter Account Information']"
        TITLE_MR = "//input[@id='id_gender1']"
        TITLE_MRS = "//input[@id='id_gender2']"
        PASSWORD_FIELD = "//input[@id='password']"
        BIRTH_DAY = "//select[@id='days']"
        BIRTH_MONTH ="//select[@id='months']"
        BIRTH_YEAR = "//select[@id='years']"
        NEWSLETTER_CHECKBOX = "//input[@id='newsletter']"
        SPECIAL_OFFERS_CHECKBOX = "//input[@id='optin']"
        #address_information
        FIRST_NAME = "//input[@id='first_name']"
        LAST_NAME = "//input[@id='last_name']"
        COMPANY = "//input[@id='company']"
        STREET_ADDRESS = "//input[@id='address1']"
        ADDRESS_2 = "//input[@id='address2']"
        COUNTRY_SELECTION ="//select[@id='country']"
        STATE = "//input[@id='state']"
        CITY = "//input[@id='city']"
        ZIPCODE = "//input[@id='zipcode']"
        MOBILE_NUMBER = "//input[@id='zipcode']"
        CREATE_ACCOUNT_BUTTON = "//button[normalize-space()='Create Account']"



    def __init__(self):
        try:
            self.selib = BuiltIn().get_library_instance("SeleniumLibrary")
        except RobotNotRunningError:
            self.selib = None
        
        # Oletusarvot asetetaan tässä. ÄLÄ lue Robot-muuttujia __init__:ssä.
        self.base_url = "https://automationexercise.com/"
        self.default_browser = "chrome"

    def _selib(self):
        if not self.selib:
            self.selib = BuiltIn().get_library_instance("SeleniumLibrary")
        return self.selib

    def __getattr__(self, name):
        return getattr(self._selib(), name)
    
    def gen_username(self, k=8):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=k))

    def gen_password(self, k=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=k))

    def gen_mobile(self, k=9):
        return ''.join(random.choices(string.digits, k=k))
    
    def gen_email(self, k=5):
        username = self.gen_username()
        email = f"{username}@example.com"
        return email


    @keyword
    def fill_signup_form(self, username, email):
        """Täyttää kirjautumissivulla nimen, sähköpostin"""
        self.selib.input_text(self.SignLoginLocators.SIGN_UP_NAME, username)
        self.selib.input_text(self.SignLoginLocators.SIGN_UP_EMAIL, email)

    @keyword
    def press_sign_up_button_safe(self, timeout="10s"):
        loc = self.SignLoginLocators.SIGN_UP_BUTTON
        self.selib.wait_until_element_is_visible(loc, timeout)
        self.selib.scroll_element_into_view(loc)

        # try normal click first
        try:
            self.selib.click_element(loc)
            return
        except ElementClickInterceptedException:
            pass

        # hide common ad iframes
        js_hide_ads = """
            document.querySelectorAll("iframe[id^='aswift'], iframe[title='Advertisement']")
                    .forEach(el => el.style.display = 'none');
        """
        self.selib.execute_javascript(js_hide_ads)

        # retry normal click
        try:
            self.selib.click_element(loc)
            return
        except ElementClickInterceptedException:
            pass

        # final: do a direct JS click on the specific WebElement
        we = self.selib.find_element(loc)
        self.selib.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", we)
        self.selib.driver.execute_script("arguments[0].click();", we)

    
    @keyword
    def on_account_info_page(self):
        """waiting that element is visible"""
        self.selib.wait_until_element_is_visible(self.SignLoginLocators.HEADER, "5s")

    @keyword
    def select_title(self, title: str):
        """Choose title of the person if MR or MRS. Capitalization ignored"""
        t = title.strip().lower()
        target = self.SignLoginLocators.TITLE_MR if t == "mr" else self.SignLoginLocators.TITLE_MRS
        value  = "Mr" if t == "mr" else "Mrs"
        self.selib.wait_until_element_is_visible(target, "5s")
        self.selib.click_element(target)
        self.selib.radio_button_should_be_set_to("title", value)

    @keyword
    def set_password(self, password: str):
        self.selib.input_text(self.SignLoginLocators.PASSWORD_FIELD, password)

    @keyword
    def set_birthdate(self, day: int, month: int, year: int):
        """Choose birth of date based on value, day: 1-31, month: 1-12 or year: 1900-2025"""
        self.selib.select_from_list_by_value(self.SignLoginLocators.BIRTH_DAY, day)
        self.selib.select_from_list_by_label(self.SignLoginLocators.BIRTH_MONTH, month)
        self.selib.select_from_list_by_value(self.SignLoginLocators.BIRTH_YEAR, year)

    @keyword
    def set_newsletter(self, subscribe: bool=True):
        """Select newsletter checkbox or not based on boolean value: True or Not"""
        if subscribe:
            self.selib.select_checkbox(self.SignLoginLocators.NEWSLETTER_CHECKBOX)
        else:
            self.selib.unselect_checkbox(self.SignLoginLocators.NEWSLETTER_CHECKBOX)

    @keyword
    def set_special_offers(self, enable: bool=True):
        if enable:
            self.selib.select_checkbox(self.SignLoginLocators.SPECIAL_OFFERS_CHECKBOX)
        else:
            self.selib.unselect_checkbox(self.SignLoginLocators.SPECIAL_OFFERS_CHECKBOX)

    @keyword
    def fill_address_info(self, first_name, last_name, company, address1, address2, country, state, city, zipcode, mobile):
        self.selib.input_text(self.SignLoginLocators.FIRST_NAME, first_name)
        self.selib.input_text(self.SignLoginLocators.LAST_NAME, last_name)
        if company:
            self.selib.input_text(self.SignLoginLocators.COMPANY, company)
        self.selib.input_text(self.SignLoginLocators.STREET_ADDRESS, address1)
        if address2:
            self.selib.input_text(self.SignLoginLocators.ADDRESS_2, address2)
        self.selib.select_from_list_by_value(self.SignLoginLocators.COUNTRY_SELECTION, country)
        self.selib.input_text(self.SignLoginLocators.STATE, state)
        self.selib.input_text(self.SignLoginLocators.CITY, city)
        self.selib.input_text(self.SignLoginLocators.ZIPCODE, zipcode)
        self.selib.input_text(self.SignLoginLocators.MOBILE_NUMBER, mobile)

    @keyword
    def submit_create_account(self, timeout="10s"):
        loc = self.SignLoginLocators.CREATE_ACCOUNT_BUTTON
        self.selib.wait_until_element_is_visible(loc, timeout)
        self.selib.scroll_element_into_view(loc)

        # try normal click first
        try:
            self.selib.click_element(loc)
            return
        except ElementClickInterceptedException:
            pass

        # hide common ad iframes
        js_hide_ads = """
            document.querySelectorAll("iframe[id^='aswift'], iframe[title='Advertisement']")
                    .forEach(el => el.style.display = 'none');
        """
        self.selib.execute_javascript(js_hide_ads)

        # retry normal click
        try:
            self.selib.click_element(loc)
            return
        except ElementClickInterceptedException:
            pass

        # final: do a direct JS click on the specific WebElement
        we = self.selib.find_element(loc)
        self.selib.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", we)
        self.selib.driver.execute_script("arguments[0].click();", we)


    @keyword
    def fill_account_information(
        self,
        title, password, day, month, year,
        first_name, last_name, company, address1, address2, country, state, city, zipcode, mobile,
        newsletter: bool=True, special_offers: bool=False
    ):
        """Testissä käytettävä korkeatason avainsana, joka käyttää aikaisempia avainsanoja"""
        try:
            self.on_account_info_page()
        except Exception:
            pass
        self.select_title(title)
        self.set_password(password)
        self.set_birthdate(day, month, year)
        self.set_newsletter(newsletter)
        self.set_special_offers(special_offers)
        self.fill_address_info(first_name, last_name, company, address1, address2, country, state, city, zipcode, mobile)

    @keyword
    def sign_up_new_user(self, **person):
        """Uuden käyttäjän luonti oletusarvoilla, tai vaihtoehtoisesti &{PERSON} muuttujalla."""
        bi = BuiltIn()
        # oletusarvot
        defaults = {
            "title": "mr", "day": "10", "month": "June", "year": "1993",
            "first": "Test", "last": "User", "company": "", "addr1": "", "addr2": "",
            "country": "India", "state": "", "city": "", "zip": "",
            "newsletter": False, "special_offers": False
        }
        defaults.update(person or {})
        p = defaults

        # generoi jos puuttuu tiedot
        username = p.get("username") or self.gen_username()
        email = p.get("email") or f"{username}@example.com"
        password = p.get("password") or self.gen_password()
        mobile = p.get("mobile") or self.gen_mobile()

        # tee Robot-muuttujiksi (tarvittaessa testin muuhun käyttöön)
        bi.set_test_variable("${USERNAME}", username)
        bi.set_test_variable("${EMAIL}", email)
        bi.set_test_variable("${PASSWORD}", password)
        bi.set_test_variable("${MOBILENUMBER}", mobile)

        # nyt täytetään lomakkeet käyttämällä p ja generoitua dataa
        HomePage = bi.get_library_instance("HomePage")
        HomePage.click_signup_login_link_from_homepage()
        self.fill_signup_form(username, email)
        self.press_sign_up_button_safe()

        self.fill_account_information(
            p["title"], password, p["day"], p["month"], p["year"],
            p["first"], p["last"], p["company"], p["addr1"], p["addr2"],
            p["country"], p["state"], p["city"], p["zip"], mobile,
            newsletter=p["newsletter"], special_offers=p["special_offers"]
        )
        self.submit_create_account()

        # palauta datat jos haluat käsitellä niitä Robot-tasolla
        return username, email, password, mobile

    @keyword
    def attempt_signup_with_existing_email(self, email, name):
        """Tries to sign up with an already-used email and verifies the error."""
        self.fill_signup_form(name, email)
        self.press_sign_up_button_safe()
        # Assert the known error text
        self.selib.wait_until_element_is_visible(
            "xpath=//p[normalize-space()='Email Address already exist!']",
            "5s"
        )