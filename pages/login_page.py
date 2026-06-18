from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for https://sauce-demo.myshopify.com/account/login"""

    EMAIL_FIELD     = (By.CSS_SELECTOR, "input[type='email'], input[name='customer[email]']")
    PASSWORD_FIELD  = (By.CSS_SELECTOR, "input[type='password'], input[name='customer[password]']")
    FORGOT_PWD_LINK = (By.LINK_TEXT, "Forgot your password?")
    SIGNUP_LINK     = (By.CSS_SELECTOR, "a[href='/account/register']")

    # Covers error containers across common Shopify theme variants.
    # ul.errors        — default_errors filter output (Timber, Debut, Minimal, Vintage)
    # .form__message   — Dawn / OS 2.0 themes
    # .notice--error   — some custom themes
    ERROR_MESSAGE = (By.CSS_SELECTOR,
        "ul.errors, "
        ".form__message, "
        ".notice--error"
    )

    # Uses action*= (contains) to handle Shopify appending ?return_url=... to the
    # action attribute at runtime, which breaks an exact [action='/account/login'] match.
    SUBMIT_BUTTON = (By.CSS_SELECTOR,
        "form[action*='/account/login'] input[type='submit'], "
        "form[action*='/account/login'] button[type='submit']"
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
        # Wait for the POST -> redirect -> page-load cycle to finish before
        # any subsequent assertion polls the DOM.
        self.wait_for_page_load()

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
        Returns True when an error message is present after a failed login.

        Two strategies are attempted in order:

        1. CSS selector — waits up to 10s for a visible, non-empty element
           matching any of the known Shopify error-container classes.

        2. JavaScript innerText fallback — scans the full page text for
           Shopify's known login error phrases. This is independent of CSS
           class names so it covers theme customisations, translated copy,
           or any structural change that breaks the element-based check.
        """
        # Strategy 1: element-based
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            if element.text.strip():
                return True
        except Exception:
            pass

        # Strategy 2: full-page text scan
        try:
            body_text = self.driver.execute_script(
                "return document.body.innerText"
            ).lower()
            shopify_error_phrases = [
                "email or password is incorrect",
                "incorrect email or password",
                "invalid email or password",
                "email address or password is incorrect",
                "unidentified customer",
            ]
            return any(phrase in body_text for phrase in shopify_error_phrases)
        except Exception:
            return False

    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)