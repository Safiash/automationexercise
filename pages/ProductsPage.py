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
        WRITE_YOUR_REVIEW="//a[normalize-space()='Write Your Review']"
        ADD_TO_CART_1="(//a[@class='btn btn-default add-to-cart'][normalize-space()='Add to cart'])"
        ADD_TO_CART_2="//button[@type='button']"
        ADDED="//h4[@class='modal-title w-100']"
        VIEW_CART="//u[normalize-space()='View Cart']"
        CONTINUE_SHOPPING = "css:button[data-dismiss='modal']"
        CART_LINK = "//a[normalize-space()='Cart']"
        PROCEED_TO_CHECKOUT="//a[@class='btn btn-default check_out']"
        ALL_ADD_TO_CART_LINKS = "css:div.productinfo a.add-to-cart"
        

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

    @keyword
    def select_product(self):
        """
        Valitsee valitun tuotteen ja painaa tuoteikkunan add to cart-nappia. 
        Tämän jälkeen siirtyy yläotsikon kautta cart-sivulle
        """
        loc = self.ProductsPageLocators.ADD_TO_CART_1
        self.selib.wait_until_element_is_visible(loc, timeout='5s')
        self.selib.scroll_element_into_view(loc)

        clicked = False

        # yritä normaali klikkaus
        try:
            self.selib.click_element(loc)
            clicked = True
        except ElementClickInterceptedException:
            clicked = False
        except Exception:
            clicked = False

        # jos ei klikattu, piilota iframet ja yritä uudelleen
        if not clicked:
            js_hide_ads = """
                document.querySelectorAll("iframe[id^='aswift'], iframe[title='Advertisement']")
                        .forEach(el => el.style.display = 'none');
            """
            try:
                self.selib.execute_javascript(js_hide_ads)
            except Exception:
                # jos JS:n suoritus epäonnistuu, jatketaan silti fallbackeihin
                pass
            # pieni tauko että DOM ehtii päivittyä
            try:
                self.selib.sleep(0.3)
            except Exception:
                pass
            try:
                self.selib.click_element(loc)
                clicked = True
            except Exception:
                clicked = False

        # jos edelleen ei klikattu, käytä suoraa JS-klikkausta
        if not clicked:
            try:
                we = self.selib.find_element(loc)
                # scroll-to-center + DOM click
                try:
                    self.selib.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", we)
                except Exception:
                    pass
                try:
                    self.selib.driver.execute_script("arguments[0].click();", we)
                    clicked = True
                except Exception:
                    clicked = False
            except Exception:
                clicked = False

        # odotetaan lisäys-ilmoitusta ja jatketaan sitten ostoskoriin riippumatta siitä, mitä click-metodia käytti
        self.wait_until_element_is_visible(self.ProductsPageLocators.ADDED, timeout='5s')
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

    @keyword
    def click_search_button(self):
        """Klikkaa tuotteen hakupainiketta"""
        self.selib.click_element(self.ProductsPageLocators.SEARCH_BUTTON)

    @keyword
    def verify_search_results(self, expected_text):
        """Varmistaa, että hakutulokset sisältävät odotetun tuotteen"""
        self.selib.page_should_contain(expected_text)

            
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
        