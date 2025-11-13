from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


class HomePage:
    ROBOT_LIBRARY_SCOPE = "SUITE"

    class HomePageLocators:
        CONSENT_COOKIES_FRONTPAGE = "//button[@aria-label='Consent']"
        FEATURED_ITEMS_TITLE = "//h2[normalize-space()='Features Items']"
        LOGO = "//img[@alt='Website for automation practice']"
        # Header links locators
        SIGNUP_LOGIN_LINK = "//a[normalize-space()='Signup / Login']"
        HOME_LINK = "//a[normalize-space()='Home']"
        CART_LINK = "//a[normalize-space()='Cart']"
        PRODUCTS_LINK = "//a[@href='/products']"
        TEST_CASES_LINK = "//a[@href='/test_cases']"
        API_LIST_LINK = "//a[@href='/api_list']"
        CONTACKT_US_LINK = "//a[normalize-space()='Contact us']"
        # Categories locators
        WOMEN_CATEGORY = "//a[normalize-space()='Women']"
        WOMEN_CATEGORY_DRESS = "//div[@id='Women']//a[contains(text(),'Dress')]"
        WOMEN_CATEGORY_TOPS = "//a[normalize-space()='Tops']"
        WOMEN_CATEGORY_SAREES = "//a[normalize-space()='Saree']"
        MEN_CATEGORY = "//a[normalize-space()='Men']"
        MEN_CATEGORY_TSHIRTS = "//a[normalize-space()='Tshirts']"
        MEN_CATEGORY_JEANS = "//a[normalize-space()='Jeans']"
        KIDS_CATEGORY = "//a[normalize-space()='Kids']"
        KIDS_CATEGORY_DRESSES = "//div[@id='Kids']//a[contains(text(),'Dress')]"
        KIDS_CATEGORY_TOPS = "//a[normalize-space()='Tops & Shirts']"
        
        
    def __init__(self):
        """Määrittää Selenium-kirjaston käytettäväksi myöhempää varten"""
        try:
            self.selib = BuiltIn().get_library_instance("SeleniumLibrary")
        except RobotNotRunningError:
            self.selib = None
        
        # Oletusarvot asetetaan tässä. ÄLÄ lue Robot-muuttujia __init__:ssä.
        self.base_url = "https://automationexercise.com/"
        self.default_browser = "chrome"

    def _selib(self):
        """Ottaa Selenium-kirjaston käyttöön"""
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
    def open_home_page(self):
        """Avaa määritellyn kotisivun ja hyväksyy evästeet"""
        self.open_url()
        self._selib().wait_until_element_is_visible(self.HomePageLocators.CONSENT_COOKIES_FRONTPAGE, timeout="5s")
        self._selib().click_element(self.HomePageLocators.CONSENT_COOKIES_FRONTPAGE)

    @keyword
    def click_home_link_from_homepage(self):
        """Klikkaa etusivulla olevaa home -linkkiä"""
        self.click_element(self.HomePageLocators.HOME_LINK)
        self.wait_until_element_is_visible(self.HomePageLocators.LOGO, timeout="5s")

    @keyword
    def click_products_link_from_homepage(self):
        """Klikkaa etusivulla olevaa products -linkkiä"""
        self.click_element(self.HomePageLocators.PRODUCTS_LINK)
        self.wait_until_page_contains("All Products", timeout="5s")
    
    @keyword
    def click_cart_link_from_homepage(self):
        """Klikkaa etusivulla olevaa cart -linkkiä"""
        self.click_element(self.HomePageLocators.CART_LINK)
        self.wait_until_page_contains("Shopping Cart", timeout="5s")

    @keyword
    def click_signup_login_link_from_homepage(self):
        """Klikkaa etusivulla olevaa Sign/Login -linkkiä"""
        self.click_element(self.HomePageLocators.SIGNUP_LOGIN_LINK)
        self.wait_until_page_contains("Login to your account", timeout="5s")

    @keyword
    def click_test_cases_link_from_homepage(self):
        """Klikkaa etusivulla olevaa Test Cases -linkkiä"""
        self.click_element(self.HomePageLocators.TEST_CASES_BUTTON)
        self.wait_until_page_contains("Test Cases", timeout="5s")

    @keyword
    def click_api_Testing_from_homepage(self):
        """Klikkaa etusivulla olevaa Api Testing -linkkiä"""
        self.click_element(self.HomePageLocators.API_LIST_BUTTON)
        self.wait_until_page_contains("APIs List for practice", timeout="5s")

    @keyword
    def click_contact_us_link_from_homepage(self):
        """Klikkaa etusivulla olevaa Contact Us -linkkiä"""
        self.click_element(self.HomePageLocators.CONTACKT_US_LINK)
        self.wait_until_page_contains("Get In Touch", timeout="5s")

    @keyword
    def click_signup_login_link_from_homepage(self):
        """Klikkaa etusivulla olevaa Signup / Login -linkkiä"""
        self.click_element(self.HomePageLocators.SIGNUP_LOGIN_LINK)
        self.wait_until_page_contains("Login to your account", timeout="5s")

    @keyword
    def check_is_featured_items_visible(self):
        """Tarkastaa onko etusivulla Featured Items -teksti näkyvissä"""
        self.element_should_be_visible(self.HomePageLocators.FEATURED_ITEMS_TITLE)

    @keyword
    def check_is_home_page_loaded(self):
        """Tarkastaa onko etusivulla oleva kotisivun logo ja Home -linkki näkyvissä"""
        self.element_should_be_visible(self.HomePageLocators.LOGO)
        self.element_should_be_visible(self.HomePageLocators.HOME_LINK)

    @keyword
    def click_category_women(self):
        """Klikkaa etusivulla olevaa Women -kategoriaa"""
        self.click_element(self.HomePageLocators.WOMEN_CATEGORY)
        self.wait_until_element_is_visible(self.HomePageLocators.WOMEN_CATEGORY_DRESS, timeout="5s")

    @keyword
    def click_category_dress_from_women(self):
        """Klikkaa alakategoriaa "Dress" Women -kategoriasta"""
        self.click_element(self.HomePageLocators.WOMEN_CATEGORY_DRESS)
        self.wait_until_page_contains("Women - Dress Products", timeout="5s")

    @keyword
    def click_category_tops_from_women(self):
        """Klikkaa alakategoriaa "Tops" Women -kategoriasta"""
        self.click_element(self.HomePageLocators.WOMEN_CATEGORY_TOPS)
        self.wait_until_page_contains("Women - Tops Products", timeout="5s")

    @keyword
    def click_category_saree_from_women(self):
        """Klikkaa alakategoriaa "Saree" Women -kategoriasta"""
        self.click_element(self.HomePageLocators.WOMEN_CATEGORY_SAREES)
        self.wait_until_page_contains("Women - Saree Products", timeout="5s")   

    @keyword
    def click_category_men(self):
        """Klikkaa etusivulla olevaa Men -kategoriaa"""
        self.click_element(self.HomePageLocators.MEN_CATEGORY)
        self.wait_until_element_is_visible(self.HomePageLocators.MEN_CATEGORY_TSHIRTS, timeout="5s")

    @keyword
    def click_category_tshirts_from_men(self):
        """Klikkaa alakategoriaa "Tshirts" men -kategoriasta"""
        self.click_element(self.HomePageLocators.MEN_CATEGORY_TSHIRTS)
        self.wait_until_page_contains("Men - Tshirts Products", timeout="5s")

    @keyword
    def click_category_jeans_from_men(self):
        """Klikkaa alakategoriaa "Jeans" men -kategoriasta"""
        self.click_element(self.HomePageLocators.MEN_CATEGORY_JEANS)
        self.wait_until_page_contains("Men - Jeans Products", timeout="5s")
    
    @keyword
    def click_category_kids(self):
        """Klikkaa etusivulla olevaa Kids -kategoriaa"""
        self.click_element(self.HomePageLocators.KIDS_CATEGORY)
        self.wait_until_element_is_visible(self.HomePageLocators.KIDS_CATEGORY_DRESSES, timeout="5s")

    @keyword
    def click_category_dress_from_kids(self):
        """Klikkaa alakategoriaa "Dress" Kids -kategoriasta"""
        self.click_element(self.HomePageLocators.KIDS_CATEGORY_DRESSES)
        self.wait_until_page_contains("Kids - Dress Products", timeout="5s")

    @keyword
    def click_category_tops_from_kids(self):
        """Klikkaa alakategoriaa "Tops & Shirts" Kids -kategoriasta"""
        self.click_element(self.HomePageLocators.KIDS_CATEGORY_TOPS)
        self.wait_until_page_contains("Kids - Tops & Shirts Products", timeout="5s")
