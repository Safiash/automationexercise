from robot.api.deco import keyword
from Common import Common


class SignLogin(Common):

    class SignLoginLocators:
        LOGIN_YOUR_ACCOUNT_TEXT = "//h2[normalize-space()='Login to your account']"
        LOGIN_EMAIL = "//input[@data-qa='login-email']"
        LOGIN_PASSWORD = "//input[@placeholder='Password']"
        LOGIN_BUTTON = "//button[normalize-space()='Login']"

        SIGN_UP_NAME = "//input[@placeholder='Name']"
        SIGN_UP_PASSWORD = "//input[@data-qa='signup-email']"
        SIGN_UP_BUTTON = "//button[normalize-space()='Signup']"
