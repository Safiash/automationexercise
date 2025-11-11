from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

class Common:
    ROBOT_LIBRARY_SCOPE = "SUITE"

    class CommonLocators:
        CONSENT_COOKIES_FRONTPAGE = "//button[@aria-label='Consent']"
        SIGNUP_LOGIN_LINK = "//a[normalize-space()='Signup / Login']"

    def __init__(self):
        try:
            self.selib = BuiltIn().get_library_instance("SeleniumLibrary")
        except RobotNotRunningError:
            self.selib = None
        self.base_url = BuiltIn().get_variable_value("${BASE_URL}", default="https://automationexercise.com/")
        self.default_browser = BuiltIn().get_variable_value("${DEFAULT_BROWSER}", default="chrome")

    def _selib(self):
        if not self.selib:
            self.selib = BuiltIn().get_library_instance("SeleniumLibrary")
        return self.selib

    def __getattr__(self, name):
        return getattr(self._selib(), name)

    @keyword
    def open_url(self, url=None, browser=None):
        url = url or self.base_url
        browser = browser or self.default_browser
        self._selib().open_browser(url, browser=browser)
        self._selib().maximize_browser_window()

    @keyword
    def open_home_page(self):
        self.open_browser(self.BASE_URL, browser="chrome")

    @keyword
    def open_home_page(self):
        self.open_browser(self.BASE_URL, browser="chrome")

    @keyword
    def get_page_title(self):
        """Palauttaa sivun otsikon (korvaa aiemman rekursiivisen get_title:n)."""
        return self._selib().get_title()

    @keyword
    def consent_cookies(self):
        self._selib().wait_until_element_is_visible(self.CommonLocators.CONSENT_COOKIES_FRONTPAGE, timeout="5s")
        self._selib().click_element(self.CommonLocators.CONSENT_COOKIES_FRONTPAGE)