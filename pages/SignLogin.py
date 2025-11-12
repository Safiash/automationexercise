import random
import string
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


class SignLogin:

    class SignLoginLocators:
        LOGIN_LINK = "//a[normalize-space()='Signup / Login']"
        LOGIN_YOUR_ACCOUNT_TEXT = "//h2[normalize-space()='Login to your account']"
        LOGIN_EMAIL = "//input[@data-qa='login-email']"
        LOGIN_PASSWORD = "//input[@placeholder='Password']"
        LOGIN_BUTTON = "//button[normalize-space()='Login']"
        LOG_OUT_BUTTON = "//a[normalize-space()='Logout']"

        SIGN_UP_NAME = "//input[@placeholder='Name']"
        SIGN_UP_EMAIL = "//input[@data-qa='signup-email']"
        SIGN_UP_BUTTON = "//button[normalize-space()='Signup']"

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

    # ===================================================
    #           --- YLÄTASON AVAINSANAT ---
    # ===================================================

    @keyword
    def login_as_valid_user(self, email, password):
        """
        Suorittaa koko sisäänkirjautumisprosessin etusivulta 
        ja varmistaa onnistumisen.
        """
        self.click_element(self.SignLoginLocators.LOGIN_LINK)
        self.wait_until_element_is_visible(self.SignLoginLocators.LOGIN_YOUR_ACCOUNT_TEXT, timeout='5s')
        self.fill_login_form(email, password)
        self.press_login_button()
        self.verify_login()

    # ===================================================
    #           --- ALATASON AVAINSANAT ---
    # ===================================================


    @keyword
    def generate_random_credentials(self):
        """Luo random kahdeksan merkkisen käyttäjänimen ja käyttää sitä myös sähköpostissa"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = f"{username}@example.com"
        return username, email

    @keyword
    def fill_signup_form(self, name, email):
        """Täyttää kirjautumissivulla nimen ja sähköpostin"""
        self.selib.input_text(self.SignLoginLocators.SIGN_UP_NAME, name)
        self.selib.input_text(self.SignLoginLocators.SIGN_UP_EMAIL, email)

    @keyword
    def press_sign_up_button(self):
        """Painaa Sign Up -nappia"""
        self.selib.click_element(self.SignLoginLocators.SIGN_UP_BUTTON)

    @keyword
    def fill_login_form(self, email, password):
        """Täyttää kirjautumissivulla sähköpostin ja salasanan"""
        self.selib.input_text(self.SignLoginLocators.LOGIN_EMAIL, email)
        self.selib.input_text(self.SignLoginLocators.LOGIN_PASSWORD, password)

    @keyword
    def press_login_button(self):
        """Painaa Login-nappia"""
        self.click_element(self.SignLoginLocators.LOGIN_BUTTON)

    @keyword
    def verify_login(self):
        """Varmistaa että login onnistui"""
        self.wait_until_element_is_visible(self.SignLoginLocators.LOG_OUT_BUTTON, timeout='5s')

    @keyword
    def press_logout_button(self):
        """Painaa Logout-nappia"""
        self.click_element(self.SignLoginLocators.LOG_OUT_BUTTON)
        self.wait_until_element_is_visible(self.SignLoginLocators.LOGIN_YOUR_ACCOUNT_TEXT, timeout='5s')

    @keyword
    def check_login_error_message_is_visible(self):
        """Tarkistaa että virheilmoitus on näkyvissä"""
        self.wait_until_page_contains("Your email or password is incorrect!", timeout='5s')

    @keyword
    def check_please_fill_all_fields_message_is_visible(self, expected_message="Please fill out this field."):
        """Tarkistaa että 'Please fill all fields!' -viesti on näkyvissä"""
        message = self.get_element_attribute(
            self.SignLoginLocators.LOGIN_EMAIL, 
            "validationMessage"
        )
        builtin = BuiltIn()
        builtin.should_be_equal_as_strings(message, expected_message)