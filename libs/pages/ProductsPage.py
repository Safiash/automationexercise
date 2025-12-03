from robot.api.deco import keyword
import string
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from selenium.common.exceptions import ElementClickInterceptedException


class ProductsPage:

    # ===================================================
    #               --- LOKAATTORIT ---
    # ===================================================
    class ProductsPageLocators:
        SEARCH_BAR = "//input[@id='search_product']"
        SEARCH_BUTTON = "//button[@id='submit_search']"
        ALL_PRODUCTS_HEADER = "//h2[@class='title text-center']"
        VIEW_PRODUCT="//div[@class='col-sm-9 padding-right']//div[2]//div[1]//div[2]//ul[1]//li[1]//a[1]"
        ADD_TO_CART_FROM_PRODUCT_WINDOW="(//a[@class='btn btn-default add-to-cart'][normalize-space()='Add to cart'])"
        ADD_TO_CART_FROM_VIEW_PRODUCT="//button[@type='button']"
        ADDED_NOTIFICATION="//h4[@class='modal-title w-100']"
        VIEW_CART="//u[normalize-space()='View Cart']"
        CONTINUE_SHOPPING = "css:button[data-dismiss='modal']"
        CART_LINK = "//a[normalize-space()='Cart']"
        PROCEED_TO_CHECKOUT="//a[@class='btn btn-default check_out']"
        ALL_ADD_TO_CART_LINKS = "css:div.productinfo a.add-to-cart"
        ALL_BRAND_LINKS = "//div[@class='brands-name']//ul//li//a"
        SUBSCRIPTION_HEADER_BOTTOM_OF_PAGE = "//h2[normalize-space()='Subscription']"
        ARROW_BUTTON = "css:a[href='#top']"
        # Hakutulosten lokaattori
        SEARCH_RESULTS_VIEW_PRODUCT = "//a[contains(text(), 'View Product')]"
        # Product view -sivun lokaattori
        WRITE_YOUR_REVIEW_TEXT ="//a[normalize-space()='Write Your Review']"
        PRODUCT_REVIEW_NAME_INPUT ="//input[@id='name']"
        PRODUCT_REVIEW_EMAIL_INPUT ="//input[@id='email']"
        PRODUCT_REVIEW_TEXTAREA ="//textarea[@id='review']"
        REVIEW_SUBMIT_BUTTON ="//button[@id='button-review']"
        REVIEW_SUCCESS_MESSAGE ="//span[normalize-space()='Thank you for your review.']"
        

    # ===================================================
    #                   --- SETUP ---
    # ===================================================
        
    def __init__(self):
        try:
            self.selib = BuiltIn().get_library_instance("SeleniumLibrary")
        except RobotNotRunningError:
            self.selib = None
        
        self.base_url = "https://automationexercise.com/"
        self.default_browser = "chrome"

    def _selib(self):
        if not self.selib:
            self.selib = BuiltIn().get_library_instance("SeleniumLibrary")
        return self.selib

    def __getattr__(self, name):
        return getattr(self._selib(), name)
    
    # ===================================================
    #           --- YLÄTASON AVAINSANAT ---
    # ===================================================

    def _safe_click(self, loc):
        """
        Yrittää klikata elementtiä usealla metodilla:
        1) normaali click_element
        2) piilottaa mainos-iframe:t ja yrittää uudelleen
        3) DOM-tason JS-click fallback
        Palauttaa True jos klikkaus onnistui, muuten False.
        """
        clicked = False

        # 1) normaali klikkausyritys
        try:
            self.selib.click_element(loc)
            return True
        except ElementClickInterceptedException:
            clicked = False
        except Exception:
            clicked = False

        # 2) piilota yleisimmät mainos-iframet ja yritä uudelleen
        js_hide_ads = """
            document.querySelectorAll("iframe[id^='aswift'], iframe[title='Advertisement']")
                    .forEach(el => el.style.display = 'none');
        """
        try:
            self.selib.execute_javascript(js_hide_ads)
        except Exception:
            pass
        try:
            # pieni tauko jotta DOM ehtii päivittyä
            try:
                self.selib.sleep(0.3)
            except Exception:
                pass
            self.selib.click_element(loc)
            return True
        except Exception:
            clicked = False

        # 3) viimeinen fallback: suora DOM click
        try:
            we = self.selib.find_element(loc)
            try:
                self.selib.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", we)
            except Exception:
                pass
            try:
                self.selib.driver.execute_script("arguments[0].click();", we)
                return True
            except Exception:
                return False
        except Exception:
            return False
        
    @keyword
    def search_product_by_name(self, product_name):
        """
        Syöttää tuotteen nimen hakukenttään ja klikkaa hakupainiketta.
        Varmistaa, että hakutulokset sisältävät odotetun tuotteen.
        """
        self.input_search_text(product_name)
        self.click_search_button()
        self.verify_search_results(product_name)


    @keyword
    def select_product(self):
        """
        Valitsee valitun tuotteen ja painaa tuoteikkunan add to cart-nappia. Tämän jälkeen siirtyy yläotsikon kautta cart-sivulle
        """
        loc = self.ProductsPageLocators.ADD_TO_CART_FROM_PRODUCT_WINDOW
        self.selib.wait_until_element_is_visible(loc, timeout='5s')
        self.selib.scroll_element_into_view(loc)

        # käytetään uudelleen käytettävää helper-metodia turvalliseen klikkaukseen
        self._safe_click(loc)

        # odotetaan lisäys-ilmoitusta ja jatketaan sitten ostoskoriin riippumatta siitä, mitä click-metodia käytti
        self.wait_until_element_is_visible(self.ProductsPageLocators.ADDED_NOTIFICATION, timeout='5s')
        self.click_element(self.ProductsPageLocators.CONTINUE_SHOPPING)
        self.wait_until_element_is_visible(self.ProductsPageLocators.CART_LINK, timeout='5s')
        self.click_element(self.ProductsPageLocators.CART_LINK)
        self.wait_until_element_is_visible(self.ProductsPageLocators.PROCEED_TO_CHECKOUT, timeout='5s')

    @keyword
    def add_products_to_cart_by_quantity(self, quantity: int):
        """
        Lisää argumenttina annetun määrän tuotteita ostoskoriin tuotesivulta.
        """

        # Otetaan 'Add to cart' -lokaattori talteen merkkijonona
        add_to_cart_selector = self.ProductsPageLocators.ALL_ADD_TO_CART_LINKS
        if add_to_cart_selector.startswith("css:"):
            add_to_cart_selector = add_to_cart_selector[4:].strip()

        # Varmistetaan, että tuotteita on tarpeeksi
        count = self.get_element_count(self.ProductsPageLocators.ALL_ADD_TO_CART_LINKS)
        if count < quantity:
            raise AssertionError(
                f"Haluttiin lisätä {quantity} tuotetta, mutta sivulla "
                f"oli vain {count} 'Add to cart' -nappia.")

        # Lisää annetun määrän tuotteita ostoskoriin
        for i in range(quantity):
            js_code_add = f"document.querySelectorAll(\"{add_to_cart_selector}\")[{i}].click();"
            
            self.execute_javascript(js_code_add)
            
            self.wait_for_product_added_modal_and_continue()
            
            # Odotetaan, että pop-up sulkeutuu ennen seuraavaa lisäystä
            self.wait_until_element_is_not_visible(
                self.ProductsPageLocators.VIEW_CART, timeout="5s")
            
    @keyword
    def write_product_review(self, name, email, review_text):
        """
        Lisää tuotearvostelun annetulla nimellä, sähköpostilla ja arvostelutekstillä.
        """
        self.add_name_to_review(name)
        self.add_email_to_review(email)
        self.add_text_to_review(review_text)

    @keyword
    def submit_review_missing_info_failure(self):
        """Klikkaa tuotearvostelun Submit -nappia ja varmistaa, että 
           arvostelu ei lähetetty nimen puuttuessa"""
        msg = "Please fill out this field."
        self.selib.click_element(self.ProductsPageLocators.REVIEW_SUBMIT_BUTTON)
        
        error = self.get_error_message_text_from_product_review(self.ProductsPageLocators.PRODUCT_REVIEW_NAME_INPUT)
        
        BuiltIn().should_be_equal(error, msg)

    @keyword
    def submit_review_missing_text_failure(self):
        """Klikkaa tuotearvostelun Submit -nappia ja varmistaa, että 
           arvostelu ei lähetetty arvostelutekstin puuttuessa"""
        msg = "Please fill out this field."
        self.selib.click_element(self.ProductsPageLocators.REVIEW_SUBMIT_BUTTON)
        
        error = self.get_error_message_text_from_product_review(self.ProductsPageLocators.PRODUCT_REVIEW_TEXTAREA)
        
        BuiltIn().should_be_equal(error, msg)

    @keyword
    def verify_all_brands_navigation(self):
        """
        Etsii kaikki brändit 'Brands'-sivupalkista, klikkaa niitä vuorotellen
        ja varmistaa, että brändin sivu aukeaa oikein.
        """
        loc = self.ProductsPageLocators.ALL_BRAND_LINKS
        
        self.selib.wait_until_element_is_visible(loc)
        # Laskee brändilinkkien määrän
        count = self.selib.get_element_count(loc)

        # Käy läpi kaikki brändit
        for i in range(1, count + 1):
            current_brand_locator = f"({loc})[{i}]"
            self.selib.wait_until_element_is_visible(current_brand_locator)
            link_text = self.selib.get_text(current_brand_locator)
            self.selib.click_element(current_brand_locator)
            self.selib.wait_until_page_contains("Brand -", timeout="5s")
            self.selib.go_back()


    # ===================================================
    #           --- ALATASON AVAINSANAT ---
    # ===================================================

    @keyword
    def input_search_text(self, text):
        """Syöttää argumenttina annettavan tekstin tuotteen hakukenttään"""
        self.selib.input_text(self.ProductsPageLocators.SEARCH_BAR, text)

    @keyword
    def open_shopping_cart(self):
        """Avaa ostoskorin klikkaamalla yläotsikon cart-linkkiä"""
        self.selib.click_element(self.ProductsPageLocators.CART_LINK)
        self.selib.wait_until_element_is_visible(
            self.ProductsPageLocators.PROCEED_TO_CHECKOUT, timeout="5s")

    def click_search_button(self):
        """Klikkaa tuotteen hakupainiketta"""
        self.selib.click_element(self.ProductsPageLocators.SEARCH_BUTTON)

    def verify_search_results(self, expected_text):
        """Varmistaa, että hakutulokset sisältävät odotetun tuotteen"""
        self.selib.page_should_contain(expected_text)

    def click_view_product_after_search(self):
        """Klikkaa haun jälkeen näkyvissä olevaa 'View Product' -linkkiä"""
        self.selib.click_element(self.ProductsPageLocators.SEARCH_RESULTS_VIEW_PRODUCT)
        self.selib.wait_until_element_is_visible(
            self.ProductsPageLocators.WRITE_YOUR_REVIEW_TEXT, timeout="5s")
            
    def wait_for_product_added_modal_and_continue(self):
        """Odottaa, että 'Product Added!' -pop up ilmestyy 
            ja klikkaa sitten 'Continue Shopping'."""
        # Otetaan 'Continue' -lokaattori talteen merkkijonona
        continue_selector = self.ProductsPageLocators.CONTINUE_SHOPPING
        if continue_selector.startswith("css:"):
            continue_selector = continue_selector[4:].strip()
        
        self.wait_until_element_is_visible(
            self.ProductsPageLocators.VIEW_CART, timeout="5s")
        
        js_code_continue = f"document.querySelector(\"{continue_selector}\").click();"

        self.execute_javascript(js_code_continue)

    def add_name_to_review(self, name):
        """Syöttää nimen tuotearvosteluun"""
        self.selib.input_text(self.ProductsPageLocators.PRODUCT_REVIEW_NAME_INPUT, name)

    def add_email_to_review(self, email):
        """Syöttää sähköpostin tuotearvosteluun"""
        self.selib.input_text(self.ProductsPageLocators.PRODUCT_REVIEW_EMAIL_INPUT, email)

    def add_text_to_review(self, review_text):
        """Syöttää arvostelutekstin tuotearvosteluun"""
        self.selib.input_text(self.ProductsPageLocators.PRODUCT_REVIEW_TEXTAREA, review_text)

    def get_error_message_text_from_product_review(self, locator):
        """Hakee tuotearvostelun virheilmoitustekstin puuttuvasta nimestä JavaScriptin avulla
        argumenttina annettavan lokaattorin perusteella"""
        element = self.selib.find_element(locator)
        validation_msg = self.selib.driver.execute_script(
            "return arguments[0].validationMessage;", element
        )
        return validation_msg

    @keyword
    def submit_review_succesfully(self):
        """Klikkaa tuotearvostelun Submit -nappia ja varmistaa, että 
           arvostelu lähetettiin onnistuneesti"""
        self.selib.click_element(self.ProductsPageLocators.REVIEW_SUBMIT_BUTTON)
        self.selib.wait_until_element_is_visible(
            self.ProductsPageLocators.REVIEW_SUCCESS_MESSAGE, timeout="5s")    

    @keyword    
    def scroll_to_the_bottom_of_page(self):
        """Selaa sivun alas loppuun asti"""
        self.selib.execute_javascript("window.scrollTo(0, document.body.scrollHeight);")

    @keyword
    def go_back_to_top_using_arrow_button(self):
        """Klikkaa sivun alareunassa näkyvää nuoli ylös -painiketta, joka vie sivun yläreunaan"""
        loc = self.ProductsPageLocators.ARROW_BUTTON
        self.selib.wait_until_element_is_visible(loc, timeout='5s')
        self.selib.click_element(loc)
        self.selib.wait_until_element_is_visible(
            self.ProductsPageLocators.ALL_PRODUCTS_HEADER, timeout='5s')

        