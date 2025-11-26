from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.libraries.BuiltIn import BuiltIn


class Cart:
    class CartPageLocators:
        PROCEED_TO_CHECKOUT="//a[@class='btn btn-default check_out']"
        ADDRESS_DETAILS="//h2[normalize-space()='Address Details']"
        PRODUCT_ROWS_IN_CART = "css:table#cart_info_table tbody tr"
        DELETE_ITEM_FROM_BASKET_BUTTON = "css:a.cart_quantity_delete"
        EMPTY_CART_MESSAGE = "css:span#empty_cart"
        

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
    def verify_product_count_in_cart(self, expected_count: int):
        """
        Varmistaa, että ostoskorissa on argumenttina annettu määrä tuoterivejä
        """
        # try:
        #     expected_count_int = int(expected_count)
        # except ValueError:
        #     raise ValueError(f"Annetun määrän '{expected_count}' pitää olla numero.")

        # 1. Odota, että taulukko on latautunut (vähintään yksi rivi löytyy)
        self.wait_until_element_is_visible(
            self.CartPageLocators.PRODUCT_ROWS_IN_CART, 
            timeout="5s"
        )
        
        # 2. Hae KAIKKI tuoterivit
        elements = self.get_webelements(self.CartPageLocators.PRODUCT_ROWS_IN_CART)
        
        # 3. Laske niiden todellinen määrä
        actual_count = len(elements)
        print(actual_count)
        
        # 4. Varmista, että määrä on oikea (käyttäen BuiltIn-kirjastoa)
        builtin = BuiltIn()
        builtin.should_be_equal_as_strings(
            actual_count, 
            expected_count
        )

    @keyword
    def empty_shopping_cart(self):
        """Tyhjentää ostoskorin ja varmistaa tyhjän korin viestin."""
        
        # Hakee puhtaan CSS-selektorin lokaattoristasi
        delete_selector = self._get_clean_css_selector(
            self.CartPageLocators.DELETE_ITEM_FROM_BASKET_BUTTON
        )

        # JavaScript-koodi, joka etsii, klikkaa ja palauttaa tilan
        js_check_and_click = f"""
            var element = document.querySelector(\"{delete_selector}\");
            if (element) {{
                element.click();
                return true;
            }}
            return false;
        """

        # Aja silmukkaa niin kauan kuin JS löytää ja klikkaa elementin
        while self.execute_javascript(js_check_and_click):
            BuiltIn().sleep("1s") 
            
        # Varmista lopuksi, että tyhjän korin viesti näkyy
        self.wait_until_element_is_visible(
            self.CartPageLocators.EMPTY_CART_MESSAGE, 
            timeout="5s"
        )

    
    # ===================================================
    #           --- ALATASON AVAINSANAT ---
    # ===================================================

    @keyword
    def proceed_to_checkout(self):
        """
        In the cart-page clicks proceed to checkout-button and then verifies that it lead to checkout
        """
        self.click_element(self.CartPageLocators.PROCEED_TO_CHECKOUT)
        self.wait_until_element_is_visible(self.CartPageLocators.ADDRESS_DETAILS, timeout='5s')

    def _get_clean_css_selector(self, locator_str: str):
        """Poistaa 'css:'-etuliitteen lokaattorista JavaScript-käyttöä varten."""
        if locator_str.startswith("css:"):
            return locator_str[4:].strip()
        return locator_str.strip()


    @keyword
    def check_cart(self):
        """
        Tarkistaa, että ostokorissa on tuote katsomalla,
        näkyykö poista tuote/poista rivi nappulaa, jos näkyvissä on empty cart ilmoitus, nostaa errorin"
        """
        selib = BuiltIn().get_library_instance("SeleniumLibrary")
        builtin = BuiltIn()

        delete_btn = self.CartPageLocators.DELETE_ITEM_FROM_BASKET_BUTTON
        empty_msg = self.CartPageLocators.EMPTY_CART_MESSAGE

        delete_visible = builtin.run_keyword_and_return_status(
            "Element Should Be Visible", delete_btn)

        if delete_visible:
            return
        
        empty_visible = builtin.run_keyword_and_return_status(
            "Element Should Be Visible", empty_msg)

        if empty_visible:
            raise AssertionError("Cart is empty — expected delete button to be visible.")

