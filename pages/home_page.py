from robot.api.deco import keyword
from SeleniumLibrary import SeleniumLibrary

class HomePage:
    def __init__(self):
        self.selib = SeleniumLibrary()

    BASE_URL = "https://automationexercise.com/"

    LOGO = "xpath://img[@alt='Automation Exercise']"
    HOME_LINK = "xpath://a[contains(.,'Home')]"
    PRODUCTS_LINK = "xpath://a[contains(.,'Products')]"
    SIGNUP_LOGIN_LINK = "xpath://a[contains(.,'Signup / Login')]"
    TEST_CASES_BUTTON = "xpath://a[contains(.,'Test Cases') and contains(@class,'btn-success')]"
    API_LIST_BUTTON = "xpath://a[contains(.,'APIs list for practice')]"
    FEATURED_ITEMS_TITLE = "xpath://h2[contains(.,'FEATURES ITEMS')]"

    @keyword
    def open_home_page(self):
        self.selib.open_browser(self.BASE_URL, browser="chrome")

    @keyword
    def is_home_page_loaded(self):
        self.selib.element_should_be_visible(self.LOGO)
        self.selib.element_should_be_visible(self.HOME_LINK)

    @keyword
    def click_test_cases(self):
        self.selib.click_element(self.TEST_CASES_BUTTON)

    @keyword
    def click_api_list(self):
        self.selib.click_element(self.API_LIST_BUTTON)
