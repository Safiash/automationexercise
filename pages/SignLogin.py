import random
import string
from robot.api.deco import keyword
from Common import Common


class SignLogin(Common):

    class SignLoginLocators:
        LOGIN_YOUR_ACCOUNT_TEXT = "//h2[normalize-space()='Login to your account']"
        LOGIN_EMAIL = "//input[@data-qa='login-email']"
        LOGIN_PASSWORD = "//input[@placeholder='Password']"
        LOGIN_BUTTON = "//button[normalize-space()='Login']"

        SIGN_UP_NAME = "//input[@placeholder='Name']"
        SIGN_UP_EMAIL = "//input[@data-qa='signup-email']"
        SIGN_UP_BUTTON = "//button[normalize-space()='Signup']"

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

    @keyword
    def fill_signup_form_with_random_user(self):
        """Use two keywords from above to create random user sign up"""
        username, email = self.generate_random_credentials()
        self.fill_signup_form(username, email)
        return username, email

    

    