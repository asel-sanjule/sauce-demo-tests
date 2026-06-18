from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for https://sauce-demo.myshopify.com/account/login"""

    EMAIL_FIELD     = (By.CSS_SELECTOR, "input[type='email'], input[name='customer[email]']")
    PASSWORD_FIELD  = (By.CSS_SELECTOR, "input[type='password'], input[name='customer[password]']")
    FORGOT_PWD_LINK = (By.LINK_TEXT, "Forgot your password?")
    SIGNUP_LINK     = (By.CSS_SELECTOR, "a[href='/account/register']")

    # ul.errors      — default_errors filter output (Timber, Debut, Minimal, Vintage)
    # .form__message — Dawn / OS 2.0 themes
    # .notice--error — some custom themes
    ERROR_MESSAGE = (By.CSS_SELECTOR,
        "ul.errors, "
        ".form__message, "
        ".notice--error"
    )

    # action*= (contains) handles Shopify appending ?return_url=... at runtime.
    SUBMIT_BUTTON = (By.CSS_SELECTOR,
        "form[action*='/account/login'] input[type='submit'], "
        "form[action*='/account/login'] button[type='submit']"
    )

    # Shopify's bot-detection CAPTCHA rotates between challenge types:
    # "drag the icon to the place where it fits", "click the shape that is
    # not like the others", etc. Detecting by challenge text breaks on every
    # rotation. The Skip button is present in every variant — use that instead.
    CAPTCHA_SKIP = (By.XPATH, "//button[normalize-space(text())='Skip']")

    def open(self):
        return super().open("/account/login")

    def enter_email(self, email: str):
        self.type_text(self.EMAIL_FIELD, email)

    def enter_password(self, password: str):
        self.type_text(self.PASSWORD_FIELD, password)

    def click_submit(self):
        self.click(self.SUBMIT_BUTTON)

    def _dismiss_captcha_if_present(self):
        """
        Shopify shows a rotating CAPTCHA challenge when it suspects a bot.
        The challenge text changes between runs so we detect by the Skip
        button, which is present in every variant. Clicking Skip lets the
        original form result (the login error) load normally.
        Uses a 3s timeout so it adds no delay when no CAPTCHA is present.
        """
        try:
            skip = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.CAPTCHA_SKIP)
            )
            skip.click()
            self.wait_for_page_load()
        except Exception:
            pass  # No CAPTCHA present — continue normally

    def attempt_login(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()
        self.wait_for_page_load()
        self._dismiss_captcha_if_present()

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

        Strategy 1: CSS selector — waits for a visible, non-empty element.
        Strategy 2: JS innerText fallback — scans for Shopify's known error
        phrases in case the theme uses different class names.
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            if element.text.strip():
                return True
        except Exception:
            pass

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