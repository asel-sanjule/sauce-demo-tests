from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for https://sauce-demo.myshopify.com/account/login"""

    # ── Locators ──────────────────────────────────────────────────────────────
    # Shopify renders login errors in <div class="errors"> after a failed POST.
    # We check for PRESENCE in DOM (not visibility) because some themes
    # render the errors container with display:none initially.

    PAGE_HEADING    = (By.CSS_SELECTOR, "h1")
    EMAIL_FIELD     = (By.CSS_SELECTOR, "input[type='email'], input[name='customer[email]']")
    PASSWORD_FIELD  = (By.CSS_SELECTOR, "input[type='password'], input[name='customer[password]']")
    SUBMIT_BUTTON   = (By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
    FORGOT_PWD_LINK = (By.LINK_TEXT, "Forgot your password?")
    ERROR_MESSAGE   = (By.CSS_SELECTOR, ".errors, [class*='errors']")
    SIGNUP_LINK     = (By.CSS_SELECTOR, "a[href='/account/register']")

    # ── Actions ───────────────────────────────────────────────────────────────

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

    # ── State checks ──────────────────────────────────────────────────────────

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
        Use presence_of_element_located (not visibility) because Shopify's
        .errors container may exist in DOM but without explicit display styling.
        """
        try:
            self.wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE))
            return True
        except Exception:
            return False

    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)