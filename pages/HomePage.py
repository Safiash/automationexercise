from robot.api.deco import keyword
from Common import Common


class HomePage(Common):

    class HomePageLocators:
        HOME_LINK = "//a[normalize-space()='Home']"
        PRODUCTS_LINK = "//a[@href='/products']"
        SIGNUP_LOGIN_LINK = "//a[normalize-space()='Signup / Login']"
        TEST_CASES_BUTTON = "//a[@href='/test_cases']"
        API_LIST_BUTTON = "//a[@href='/api_list']"
        FEATURED_ITEMS_TITLE = "//h2[normalize-space()='Features Items']"
        LOGO = "//img[@alt='Website for automation practice']"

    @keyword
    def open_home_page(self):
        self.open_url()

    @keyword
    def click_home(self):
        self.click_element(self.HomePageLocators.HOME_LINK)

    @keyword
    def click_products(self):
        self.click_element(self.HomePageLocators.PRODUCTS_LINK)

    @keyword
    def click_signup_login(self):
        self.click_element(self.HomePageLocators.SIGNUP_LOGIN_LINK)

    @keyword
    def click_test_cases(self):
        self.click_element(self.HomePageLocators.TEST_CASES_BUTTON)

    @keyword
    def click_api_list(self):
        self.click_element(self.HomePageLocators.API_LIST_BUTTON)

    @keyword
    def is_featured_items_visible(self):
        self.element_should_be_visible(self.HomePageLocators.FEATURED_ITEMS_TITLE)

    @keyword
    def is_home_page_loaded(self):
        self.element_should_be_visible(self.HomePageLocators.LOGO)
        self.element_should_be_visible(self.HomePageLocators.HOME_LINK)
