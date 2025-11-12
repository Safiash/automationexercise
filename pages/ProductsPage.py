from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

class ProductsPage:

    class ProductsPageLocators:
        SEARCH_BAR = "//input[@id='search_product']"
        SEARCH_BUTTON = "//button[@id='submit_search']"

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