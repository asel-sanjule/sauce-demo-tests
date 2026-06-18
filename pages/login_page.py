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

    # The Skip button text is stable across all CAPTCHA challenge variants
    # ("drag the icon", "click the shape", "find all vehicles", etc.)
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
        Shopify's bot-detection CAPTCHA widget is rendered inside an iframe.
        Searching for the Skip button in the main document context never finds
        it — we must switch into each iframe in turn until we locate and click it.

        Flow:
          1. Collect all iframes currently in the main document.
          2. For each iframe, switch context and look for the Skip button (1s budget).
          3. If found — click, switch back to default content, wait for page load.
          4. If not found — switch back and try the next iframe.
          5. Always restore default content whether we succeed or not.
        """
        try:
            iframes = WebDriverWait(self.driver, 3).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
            )
        except Exception:
            return  # No iframes — no CAPTCHA present

        for iframe in iframes:
            try:
                self.driver.switch_to.frame(iframe)
                skip = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.CAPTCHA_SKIP)
                )
                skip.click()
                self.driver.switch_to.default_content()
                self.wait_for_page_load()
                return  # Done — CAPTCHA dismissed
            except Exception:
                self.driver.switch_to.default_content()
                continue  # Try the next iframe

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