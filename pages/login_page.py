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
    ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        "ul.errors, "
        ".form__message, "
        ".notice--error"
    )

    # action*= (contains) handles Shopify appending ?return_url=... at runtime.
    SUBMIT_BUTTON = (
        By.CSS_SELECTOR,
        "form[action*='/account/login'] input[type='submit'], "
        "form[action*='/account/login'] button[type='submit']"
    )

    # Iframe src patterns that identify known CAPTCHA / bot-gate providers.
    CAPTCHA_IFRAME = (
        By.CSS_SELECTOR,
        "iframe[src*='arkoselabs'], "
        "iframe[src*='funcaptcha'], "
        "iframe[title*='challenge'], "
        "iframe[title*='captcha']"
    )

    # Button text variants seen across Arkose Labs challenge types.
    _CAPTCHA_BUTTON_XPATHS = [
        "//button[normalize-space(text())='Skip']",
        "//button[normalize-space(text())='Verify']",
        "//button[normalize-space(text())=\"I'm not a robot\"]",
    ]

    # Inline (non-iframe) CAPTCHA elements used by some themes / providers.
    CAPTCHA_INLINE = (
        By.CSS_SELECTOR,
        "[class*='captcha'], [id*='captcha'], "
        "[class*='challenge'], [id*='challenge']"
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
        Returns True when any bot-gate / CAPTCHA widget is detected.

        Three strategies in order of cheapness:

        1. Iframe src — matches known provider URLs without switching context.
        2. Inline elements — catches non-iframe CAPTCHA renderers.
        3. Button scan — switches into every iframe and looks for known
           challenge button text (Skip / Verify / I'm not a robot).
           Per-iframe timeout is 3 s to allow for CI network latency.
        """
        # Strategy 1: provider iframe src (cheapest — no context switch)
        try:
            if self.driver.find_elements(*self.CAPTCHA_IFRAME):
                return True
        except Exception:
            pass

        # Strategy 2: inline CAPTCHA elements
        try:
            elements = self.driver.find_elements(*self.CAPTCHA_INLINE)
            if any(e.is_displayed() for e in elements):
                return True
        except Exception:
            pass

        # Strategy 3: button text inside iframes
        try:
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                try:
                    self.driver.switch_to.frame(iframe)
                    for xpath in self._CAPTCHA_BUTTON_XPATHS:
                        try:
                            WebDriverWait(self.driver, 3).until(
                                EC.presence_of_element_located((By.XPATH, xpath))
                            )
                            return True
                        except Exception:
                            pass
                except Exception:
                    pass
                finally:
                    self.driver.switch_to.default_content()
        except Exception:
            pass

        return False

    def login_was_rejected(self) -> bool:
        """
        Returns True if Shopify did not grant account access.

        Uses URL as the primary signal rather than DOM content, because
        Shopify's response in CI headless sessions varies:

          /account/login  → stayed on login page, inline error shown
          /challenge, etc → bot-gate / challenge page fired (no /account)
          /account        → login succeeded (this method returns False)

        A successful Shopify login always redirects to /account (dashboard).
        Any URL that is not /account — including /account/login — therefore
        means the login was blocked, regardless of which mechanism fired.

        DOM checks (error message, CAPTCHA) follow as supplementary signals
        for cases where the redirect hasn't completed or JS is still painting.
        """
        current_url = self.driver.current_url

        # Stayed on login page — most common rejection path
        if "/account/login" in current_url:
            return True

        # Redirected somewhere other than the account dashboard —
        # challenge page, Cloudflare gate, interstitial, etc.
        if "/account" not in current_url:
            return True

        # On an /account URL but may still have an inline error or CAPTCHA
        # overlaid before granting dashboard access (edge case).
        return self.has_error_message() or self.is_captcha_present()

    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
