from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


class ContactUs:

        class ContactUsLocators:
            CONTACT_US_NAME = "//input[@placeholder='Name']"
            CONTACT_US_EMAIL = "//input[@placeholder='Email']"
            CONTACT_US_SUBJECT = "//input[@placeholder='Subject']"
            CONTACT_US_MESSAGE = "//textarea[@id='message']"
            CONTACT_US_SUBMIT = "//input[@name='submit']"

        def __init__(self):
        # Alusta selib Noneksi
            self.selib = None

        def _selib(self):
        # Lataa SeleniumLibrary vain kerran ja tallenna se self.selib-muuttujaan
            if not self.selib:
                try:
                    self.selib = BuiltIn().get_library_instance("SeleniumLibrary")
                except RobotNotRunningError:
                    # Käsittele tilanne, jos luokkaa kutsutaan Robot Frameworkin ulkopuolella
                    pass 
            return self.selib

        def __getattr__(self, name):
            # Delegoi puuttuvat avainsanat SeleniumLibrarylle
            return getattr(self._selib(), name)

        @keyword
        def submit_name(self, name):
                """Täyttää nimen contact us -lomakkeeseen"""
                self.selib.input_text(self.ContactUsLocators.CONTACT_US_NAME, name)

        @keyword
        def submit_email_contactus(self, email):
            """Täyttää sähköpostiosoitteen contact us -lomakkeeseen"""
            self.selib.input_text(self.ContactUsLocators.CONTACT_US_EMAIL, email)

        @keyword
        def submit_subject(self, subject):
            """Täyttää viestin otsikon contact us -lomakkeeseen"""
            self.selib.input_text(self.ContactUsLocators.CONTACT_US_SUBJECT, subject)

        @keyword
        def submit_message(self, message):
            """Täyttää tekstiosion contact us -lomakkeeseen"""
            self.selib.input_text(self.ContactUsLocators.CONTACT_US_MESSAGE, message)

        @keyword
        def submit_contact_us(self):
            """Lähettää contact us -lomakkeen"""
            self.click_element(self.ContactUsLocators.CONTACT_US_SUBMIT)
            self.selib.handle_alert("ACCEPT")