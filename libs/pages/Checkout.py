from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from selenium.common.exceptions import ElementClickInterceptedException


class Checkout:


    # ===================================================
    #               --- LOKAATTORIT ---
    # ===================================================
    class Checkoutlocators:
        PLACE_ORDER="//a[@class='btn btn-default check_out']"
        PAYMENT="//h2[@class='heading']"

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
    
    # ===================================================
    #           --- YLÄTASON AVAINSANAT ---
    # ===================================================


    # ===================================================
    #           --- ALATASON AVAINSANAT ---
    # ===================================================
    
    @keyword
    def place_order(self):
        """
        Painaa place order-nappulaa ja odottaa että payment-otsikko tulee näkyviin.
        """
        self.click_element(self.Checkoutlocators.PLACE_ORDER)
        self.wait_until_element_is_visible(self.Checkoutlocators.PAYMENT, timeout='5s')
