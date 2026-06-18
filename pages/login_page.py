from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for https://sauce-demo.myshopify.com/account/login"""

    EMAIL_FIELD     = (By.CSS_SELECTOR, "input[type='email'], input[name='customer[email]']")
    PASSWORD_FIELD  = (By.CSS_SELECTOR, "input[type='password'], input[name='customer[password]']")
    FORGOT_PWD_LINK = (By.LINK_TEXT, "Forgot your password?")
    SIGNUP_LINK     = (By.CSS_SELECTOR, "a[href='/account/register']")
    ERROR_MESSAGE   = (By.CSS_SELECTOR, ".errors, [class*='errors']")

    # Scoped to the login form specifically — prevents matching the search bar's
    # submit button, which also uses input[type='submit'] and caused tests to
    # navigate to /search?type=product&q= instead of submitting the login form.
    SUBMIT_BUTTON = (By.CSS_SELECTOR,
        "form[action='/account/login'] input[type='submit'], "
        "form[action='/account/login'] button[type='submit']"
    )

    def open(self):
        return super().open("/account/login")

    def enter_email(self, email: str):
        self.type_text(self.EMAIL_FIELD, email)

    def enter_password(self, password: str):
        self.type_text(self.PASSWORD_FIELD, password)

    def click_submit(self):
        self.click(self.SUBMIT_BUTTON)

    def attempt_login(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()
		self.wait_for_page_load()   # new helper added to BasePage

    def is_email_field_present(self) -> bool:
        return self.is_visible(self.EMAIL_FIELD)

    def is_password_field_present(self) -> bool:
        return self.is_visible(self.PASSWORD_FIELD)

    def is_submit_button_present(self) -> bool:
        return self.is_visible(self.SUBMIT_BUTTON)

    def is_forgot_password_link_present(self) -> bool:
        return self.is_visible(self.FORGOT_PWD_LINK)

    def has_error_message(self) -> bool:
        """
        Use presence_of_element_located (not visibility) — Shopify renders
        the .errors container in the DOM before errors are added to it.
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
			return bool(element.text.strip())
        except Exception:
            return False

    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)