import random
import string
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
#from HomePage import HomePage


class SignLogin:

    class SignLoginLocators:
        LOGIN_YOUR_ACCOUNT_TEXT = "//h2[normalize-space()='Login to your account']"
        LOGIN_EMAIL = "//input[@data-qa='login-email']"
        LOGIN_PASSWORD = "//input[@placeholder='Password']"
        LOGIN_BUTTON = "//button[normalize-space()='Login']"

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

    @keyword
    def generate_random_credentials(self):
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = f"{username}@example.com"
        return username, email

    @keyword
    def fill_signup_form(self, name, email):
        self.selib.input_text(self.SignLoginLocators.SIGN_UP_NAME, name)
        self.selib.input_text(self.SignLoginLocators.SIGN_UP_EMAIL, email)
        self.selib.click_element(self.SignLoginLocators.SIGN_UP_BUTTON)

    