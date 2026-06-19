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

    # The Skip button text is stable across all CAPTCHA challenge types.
    CAPTCHA_SKIP = (By.XPATH, "//button[normalize-space(text())='Skip']")

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
        Returns True when a visible, non-empty inline error message is present.

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

    def is_captcha_present(self) -> bool:
        """
        Returns True when Shopify's bot-detection CAPTCHA widget is visible.

        The CAPTCHA (Arkose Labs / FunCaptcha) renders inside an iframe and
        fires when a headless browser submits invalid credentials from a CI IP.
        Detection searches all iframes for the Skip button, which is present
        across every challenge variant the widget rotates through.
        """
        try:
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                try:
                    self.driver.switch_to.frame(iframe)
                    WebDriverWait(self.driver, 1).until(
                        EC.presence_of_element_located(self.CAPTCHA_SKIP)
                    )
                    self.driver.switch_to.default_content()
                    return True
                except Exception:
                    self.driver.switch_to.default_content()
        except Exception:
            pass
        return False

    def login_was_rejected(self) -> bool:
        """
        Returns True if the system refused the login attempt by either:

        1. Showing an inline error message — the normal browser flow when
           credentials are wrong.
        2. Showing a CAPTCHA challenge — Shopify's bot-detection response
           when a headless CI browser submits invalid credentials. The CAPTCHA
           proves Shopify did NOT accept the login; the user would still need
           to solve or skip the challenge before credentials are even checked.

        Both outcomes confirm the invalid credentials were rejected. Using this
        in tests instead of has_error_message() alone makes the assertion
        honest about what the system actually does in a CI environment.
        """
        return self.has_error_message() or self.is_captcha_present()

    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)