from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


class Common:
    class CommonLocators:
        CONSENT_COOKIES_FRONTPAGE = "//button[@aria-label='Consent']"

    def __init__(self):
        try:
            self.selib = BuiltIn().get_library_instance('SeleniumLibrary')
        except RobotNotRunningError:
            self.selib = None

    def _get_selib(self):
        if not self.selib:
            self.selib = BuiltIn().get_library_instance('SeleniumLibrary')
        return self.selib

    def __getattr__(self, name):
        selib = self._get_selib()
        return getattr(selib, name)

    @keyword
    def open_url(self, url):
        self.go_to(url)

    @keyword
    def get_title(self):
        return self.get_title()

    @keyword
    def consent_cookies(self):
        self.wait_until_element_is_visible(self.CommonLocators.CONSENT_COOKIES_FRONTPAGE, timeout=5)
        self.click_element(self.CommonLocators.CONSENT_COOKIES_FRONTPAGE)
