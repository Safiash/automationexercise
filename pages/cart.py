from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


class Cart:
    class Cartlocators:
        PROCEED_TO_CHECKOUT="//a[@class='btn btn-default check_out']"
        ADDRESS_DETAILS="//h2[normalize-space()='Address Details']"
    
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
    def proceed_to_checkout(self):
        """
        In the cart-page clicks proceed to checkout-button and then verifies that it lead to checkout
        """
        self.click_element(self.Cartlocators.PROCEED_TO_CHECKOUT)
        self.wait_until_element_is_visible(self.Cartlocators.ADDRESS_DETAILS, timeout='5s')