from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
import random
import string


class HomePage:
    ROBOT_LIBRARY_SCOPE = "SUITE"

    # ===================================================
    #               --- LOKAATTORIT ---
    # ===================================================
    class HomePageLocators:
        # Yleiset lokaattorit
        CONSENT_COOKIES_FRONTPAGE = "//button[@aria-label='Consent']"
        FEATURED_ITEMS_TITLE = "//h2[normalize-space()='Features Items']"
        LOGO = "//img[@alt='Website for automation practice']"
        # Header lokaattorit
        SIGNUP_LOGIN_LINK = "//a[normalize-space()='Signup / Login']"
        HOME_LINK = "//a[normalize-space()='Home']"
        CART_LINK = "//a[normalize-space()='Cart']"
        PRODUCTS_LINK = "//a[@href='/products']"
        TEST_CASES_LINK = "//a[@href='/test_cases']"
        API_LIST_LINK = "//a[@href='/api_list']"
        CONTACT_US_LINK = "//a[normalize-space()='Contact us']"
        # Kategoria ja alikategoria lokaattorit
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
        # Muut etusivun lokaattorit
        SUBMIT_EMAIL = "//input[@id='susbscribe_email']"
        SUBSCRIBE_NEWSLETTER = "//*[@id='subscribe']"
        RECOMMENDED_ITEMS_HEADER = "//h2[normalize-space()='recommended items']"
        RECOMMENDED_SHIRT_ID_NUMBER="//div[@class='item active']//h2[contains(text(),'Rs. 500')]"
        ADD_TO_CART_BUTTON="//div[@class='item active']//div[1]//div[1]//div[1]//div[1]//a[1]"
        ADDED_TO_CART_NOTIFICATION="//h4[@class='modal-title w-100']"
        VIEW_CART_FROM_NOTIFICATION="//u[normalize-space()='View Cart']"
        PROCEED_TO_CHECKOUT="//a[@class='btn btn-default check_out']"
    
    # ===================================================
    #                   --- SETUP ---
    # ===================================================
        
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
        
    def _perform_open_browser(self, url, browser, headless_mode):
        """
        Sisäinen metodi selaimen avaamiseen.
        Hoitaa ikkunan koon eri tavalla headless- ja näkyvässä tilassa.
        """
        robot_base_url = BuiltIn().get_variable_value("${BASE_URL}", default=self.base_url)
        robot_browser = BuiltIn().get_variable_value("${DEFAULT_BROWSER}", default=self.default_browser)

        url_to_open = url or robot_base_url
        browser_to_use = browser or robot_browser
        
        options_list = []
        
        if 'chrome' in browser_to_use.lower():
            # Yleiset asetukset
            options_list.append("add_argument('--disable-search-engine-choice-screen')")
            options_list.append("add_argument('--no-sandbox')")
            options_list.append("add_argument('--disable-gpu')")
            
            if headless_mode:
                # Headless-tilassa tarvitaan kiinteä koko ja headless-vipu
                options_list.append("add_argument('--headless=new')")
                options_list.append("add_argument('--window-size=1920,1080')")
            else:
                # Näkyvässä tilassa EI aseteta kiinteää kokoa tässä
                pass
        
        elif 'firefox' in browser_to_use.lower():
            if headless_mode:
                options_list.append("add_argument('--headless')")
                options_list.append("add_argument('--width=1920')")
                options_list.append("add_argument('--height=1080')")

        # Luodaan options-merkkijono
        final_options = ";".join(options_list)

        # Avataan selain
        self._selib().open_browser(url_to_open, browser=browser_to_use, options=final_options)

        # Jos ollaan NÄKYVÄSSÄ tilassa, maksimoidaan ikkuna nyt
        if not headless_mode:
            self._selib().maximize_browser_window()
    
    # ===================================================
    #           --- YLÄTASON AVAINSANAT ---
    # ===================================================

    @keyword
    def open_url(self, url=None, browser=None):
        """
        Avaa selaimen NÄKYVÄSSÄ tilassa.
        """
        self._perform_open_browser(url, browser, headless_mode=False)

    @keyword
    def open_url_headless(self, url=None, browser=None):
        """
        Avaa selaimen HEADLESS-tilassa (tausta-ajo).
        """
        self._perform_open_browser(url, browser, headless_mode=True)

    @keyword
    def open_home_page(self, headless=False):
        """
        Avaa määritellyn kotisivun ja hyväksyy evästeet.
        
        Argumentit:
        - headless: Jos True, avataan headless-tilassa. Oletus False (näkyvä).
        """
        if headless:
            self.open_url_headless()
        else:
            self.open_url()
            
        self._selib().wait_until_element_is_visible(self.HomePageLocators.CONSENT_COOKIES_FRONTPAGE, timeout="5s")
        self._selib().click_element(self.HomePageLocators.CONSENT_COOKIES_FRONTPAGE)

    @keyword
    def click_category_dress_from_women(self):
        """Klikkaa alakategoriaa "Dress" Women -kategoriasta"""
        self.click_category_women()
        self.click_element(self.HomePageLocators.WOMEN_CATEGORY_DRESS)
        self.wait_until_page_contains("Women - Dress Products", timeout="5s")

    @keyword
    def click_category_tops_from_women(self):
        """Klikkaa alakategoriaa "Tops" Women -kategoriasta"""
        self.click_category_women()
        self.click_element(self.HomePageLocators.WOMEN_CATEGORY_TOPS)
        self.wait_until_page_contains("Women - Tops Products", timeout="5s")

    @keyword
    def click_category_saree_from_women(self):
        """Klikkaa alakategoriaa "Saree" Women -kategoriasta"""
        self.click_category_women()
        self.click_element(self.HomePageLocators.WOMEN_CATEGORY_SAREES)
        self.wait_until_page_contains("Women - Saree Products", timeout="5s")   

    @keyword
    def click_category_tshirts_from_men(self):
        """Klikkaa alakategoriaa "Tshirts" men -kategoriasta"""
        self.click_category_men()
        self.click_element(self.HomePageLocators.MEN_CATEGORY_TSHIRTS)
        self.wait_until_page_contains("Men - Tshirts Products", timeout="5s")

    @keyword
    def click_category_jeans_from_men(self):
        """Klikkaa alakategoriaa "Jeans" men -kategoriasta"""
        self.click_category_men()
        self.click_element(self.HomePageLocators.MEN_CATEGORY_JEANS)
        self.wait_until_page_contains("Men - Jeans Products", timeout="5s")

    @keyword
    def click_category_dress_from_kids(self):
        """Klikkaa alakategoriaa "Dress" Kids -kategoriasta"""
        self.click_category_kids()
        self.click_element(self.HomePageLocators.KIDS_CATEGORY_DRESSES)
        self.wait_until_page_contains("Kids - Dress Products", timeout="5s")

    @keyword
    def click_category_tops_from_kids(self):
        """Klikkaa alakategoriaa "Tops & Shirts" Kids -kategoriasta"""
        self.click_category_kids()
        self.click_element(self.HomePageLocators.KIDS_CATEGORY_TOPS)
        self.wait_until_page_contains("Kids - Tops & Shirts Products", timeout="5s")

    def choose_recommended_item(self):
        """
        Valitsee suositelluista tuotteista paidan, lisää ostokoriin ja menee
        lisätty ostokoriin-ilmoituksen ostokori-sivulle.
        """
        self.click_element(self.HomePageLocators.ADD_TO_CART_BUTTON)
        self.wait_until_element_is_visible(self.HomePageLocators.ADDED_TO_CART_NOTIFICATION, timeout="5s")
        self.click_element(self.HomePageLocators.VIEW_CART_FROM_NOTIFICATION)
        self.wait_until_element_is_visible(self.HomePageLocators.PROCEED_TO_CHECKOUT, timeout='5s')


    # ===================================================
    #           --- ALATASON AVAINSANAT ---
    # ===================================================

    def get_page_title(self):
        """Palauttaa sivun otsikon."""
        return self._selib().get_title()

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
        self.click_element(self.HomePageLocators.CONTACT_US_LINK)
        self.wait_until_page_contains("Get In Touch", timeout="5s")

    @keyword
    def click_logo_from_homepage(self):
        """Klikkaa etusivulla olevaa logoa"""
        self.click_element(self.HomePageLocators.LOGO)
        self.wait_until_element_is_visible(self.HomePageLocators.LOGO, timeout="5s")

    @keyword
    def click_signup_login_link_from_homepage(self):
        """Klikkaa etusivulla olevaa Signup / Login -linkkiä"""
        self.click_element(self.HomePageLocators.SIGNUP_LOGIN_LINK)
        self.wait_until_page_contains("Login to your account", timeout="5s")

    @keyword
    def check_is_featured_items_visible(self):
        """Tarkastaa onko etusivulla Featured Items -teksti näkyvissä"""
        self.element_should_be_visible(self.HomePageLocators.FEATURED_ITEMS_TITLE)

    def check_is_home_page_loaded(self):
        """Tarkastaa onko etusivulla oleva kotisivun logo ja Home -linkki näkyvissä"""
        self.element_should_be_visible(self.HomePageLocators.LOGO)
        self.element_should_be_visible(self.HomePageLocators.HOME_LINK)

    def click_category_women(self):
        """Klikkaa etusivulla olevaa Women -kategoriaa"""
        self.click_element(self.HomePageLocators.WOMEN_CATEGORY)
        self.wait_until_element_is_visible(self.HomePageLocators.WOMEN_CATEGORY_DRESS, timeout="5s")

    def click_category_men(self):
        """Klikkaa etusivulla olevaa Men -kategoriaa"""
        self.click_element(self.HomePageLocators.MEN_CATEGORY)
        self.wait_until_element_is_visible(self.HomePageLocators.MEN_CATEGORY_TSHIRTS, timeout="5s")
    
    def click_category_kids(self):
        """Klikkaa etusivulla olevaa Kids -kategoriaa"""
        self.click_element(self.HomePageLocators.KIDS_CATEGORY)
        self.wait_until_element_is_visible(self.HomePageLocators.KIDS_CATEGORY_DRESSES, timeout="5s")

    def submit_email_newsletter(self, email):
        """Syöttää käyttäjän sähköpostiosoitteen lomakkeeseen"""
        self.selib.input_text(self.HomePageLocators.SUBMIT_EMAIL, email)

    def subscribe_newsletter(self):
        """Tilaa uutiskirjeen, kun sähköpostiosoite on jo laitettu"""
        self.click_element(self.HomePageLocators.SUBSCRIBE_NEWSLETTER)
        self.wait_until_element_is_visible(self.HomePageLocators.SUBSCRIBE_NEWSLETTER, timeout="5s")

    def gen_email(pituus=8):
        merkit = string.ascii_lowercase + string.digits
        username = "".join(random.choice(merkit) for _ in range(pituus))
        domain = "test.com"
        return f"{username}@{domain}"
    
    
    def scroll_down(self):
        """
        Skrollaa ensin sivulla recommended items-tuotteiden luokse ja tarkistaa että näkyykö paidan id-numero
        """
        self.scroll_element_into_view(self.HomePageLocators.RECOMMENDED_ITEMS_HEADER)
        self.wait_until_element_is_visible(self.HomePageLocators.RECOMMENDED_SHIRT_ID_NUMBER, timeout="5s")

    


