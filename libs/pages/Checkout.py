from robot.api.deco import keyword
from SeleniumLibrary import SeleniumLibrary
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from selenium.common.exceptions import ElementClickInterceptedException


class Checkout:
    class Checkoutlocators:
        PLACE_ORDER="//a[@class='btn btn-default check_out']"
        PAYMENT="//h2[@class='heading']"
        DELIVERY_ADDRESS = "//ul[@id='address_delivery']//li[contains(@class,'address_address1') and normalize-space()!='']"
    
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
    def place_order(self):
        self.click_element(self.Checkoutlocators.PLACE_ORDER)
        self.wait_until_element_is_visible(self.Checkoutlocators.PAYMENT, timeout='5s')

    @keyword
    def address_line1_should_match_registration(self):
        """Tarkistetaan onko osoite kassalla sama kuin rekisteröintivaiheessa"""
        bi = BuiltIn()
        expected_addr1 = bi.get_variable_value("${ADDRESS1}")
        actual_addr1 = self.selib.get_text(self.Checkoutlocators.DELIVERY_ADDRESS)
        bi.log_to_console(f"EXPECTED ADDRESS1: '{expected_addr1}'")
        bi.log_to_console(f"ACTUAL ADDRESS1:   '{actual_addr1}'")
        bi.should_be_equal(actual_addr1, expected_addr1)