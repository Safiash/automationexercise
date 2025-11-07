from robot.api.deco import keyword
from SeleniumLibrary import SeleniumLibrary

class BasePage:
    def __init__(self):
        self.selib = SeleniumLibrary()

    @keyword
    def open_url(self, url):
        self.selib.go_to(url)

    @keyword
    def get_title(self):
        return self.selib.get_title()
