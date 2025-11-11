from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


class HomePage:
    ROBOT_LIBRARY_SCOPE = "SUITE"

    class HomePageLocators:
        CONSENT_COOKIES_FRONTPAGE = "//button[@aria-label='Consent']"
        SIGNUP_LOGIN_LINK = "//a[normalize-space()='Signup / Login']"
        HOME_LINK = "//a[normalize-space()='Home']"
        PRODUCTS_LINK = "//a[@href='/products']"
        TEST_CASES_BUTTON = "//a[@href='/test_cases']"
        API_LIST_BUTTON = "//a[@href='/api_list']"
        FEATURED_ITEMS_TITLE = "//h2[normalize-space()='Features Items']"
        LOGO = "//img[@alt='Website for automation practice']"

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
    def open_url(self, url=None, browser=None):
        """
        Avaa selaimen.
        
        Lukee ${BASE_URL} ja ${DEFAULT_BROWSER} muuttujat Robot Frameworkista,
        jos niitä ei ole annettu argumentteina.
        """
        # Lue muuttujat Robotista TÄÄLLÄ (keywordin sisällä).
        robot_base_url = BuiltIn().get_variable_value("${BASE_URL}", default=self.base_url)
        robot_browser = BuiltIn().get_variable_value("${DEFAULT_BROWSER}", default=self.default_browser)

        # Käytä joko argumenttina annettua arvoa (url) tai Robotin muuttujaa (robot_base_url)
        url_to_open = url or robot_base_url
        browser_to_use = browser or robot_browser
        
        self._selib().open_browser(url_to_open, browser=browser_to_use)
        self._selib().maximize_browser_window()

    @keyword
    def get_page_title(self):
        """Palauttaa sivun otsikon."""
        return self._selib().get_title()

    @keyword
    def consent_cookies(self):
        self._selib().wait_until_element_is_visible(self.HomePageLocators.CONSENT_COOKIES_FRONTPAGE, timeout="5s")
        self._selib().click_element(self.HomePageLocators.CONSENT_COOKIES_FRONTPAGE)

    @keyword
    def open_home_page(self):
        # Tämä kutsuu nyt korjattua 'open_url' -metodia ilman argumentteja,
        # jolloin se käyttää Robot-muuttujia tai oletusarvoja.
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