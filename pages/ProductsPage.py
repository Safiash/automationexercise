from robot.api.deco import keyword
import string
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from selenium.common.exceptions import ElementClickInterceptedException


class ProductsPage:

    class ProductsPageLocators:
        SEARCH_BAR = "//input[@id='search_product']"
        SEARCH_BUTTON = "//button[@id='submit_search']"
        ALL_PRODUCTS_HEADER ="//h2[@class='title text-center']"
        VIEW_PRODUCT="//div[@class='col-sm-9 padding-right']//div[2]//div[1]//div[2]//ul[1]//li[1]//a[1]"
        WRITE_YOUR_REVIEW="//a[normalize-space()='Write Your Review']"
        ADD_TO_CART_1="(//a[@class='btn btn-default add-to-cart'][normalize-space()='Add to cart'])"
        ADD_TO_CART_2="//button[@type='button']"
        ADDED="//h4[@class='modal-title w-100']"
        VIEW_CART="//u[normalize-space()='View Cart']"
        CONTINUE_SHOPPING="//button[@class='btn btn-success close-modal btn-block']"
        CART_LINK = "//a[normalize-space()='Cart']"
        PROCEED_TO_CHECKOUT="//a[@class='btn btn-default check_out']"
        
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
    
    @keyword
    def input_search_text(self, text):
        """Syöttää tekstin tuotteen hakukenttään"""
        self.selib.input_text(self.ProductsPageLocators.SEARCH_BAR, text)

    @keyword
    def click_search_button(self):
        """Klikkaa tuotteen hakupainiketta"""
        self.selib.click_element(self.ProductsPageLocators.SEARCH_BUTTON)

    @keyword
    def verify_search_results(self, expected_text):
        """Varmistaa, että hakutulokset sisältävät odotetun tuotteen"""
        self.selib.page_should_contain(expected_text)

    @keyword
    def select_product(self):
        """
        Valitsee valitun tuotteen ja painaa tuoteikkunan add to cart-nappia. Tämän jälkeen siirtyy yläotsikon kautta cart-sivulle
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


    