from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for https://sauce-demo.myshopify.com/account/login"""

    EMAIL_FIELD     = (By.CSS_SELECTOR, "input[type='email'], input[name='customer[email]']")
    PASSWORD_FIELD  = (By.CSS_SELECTOR, "input[type='password'], input[name='customer[password]']")
    FORGOT_PWD_LINK = (By.LINK_TEXT, "Forgot your password?")
    SIGNUP_LINK     = (By.CSS_SELECTOR, "a[href='/account/register']")

    # Broad selector covering error containers across common Shopify theme variants:
    #   ul.errors          — Debut, Minimal, and most classic themes
    #   .notice--error     — some custom/modified themes
    #   [data-form-status] — some Shopify 2.0 themes
    # [class*='error'] is intentionally EXCLUDED — too greedy, matches
    # non-message elements such as input wrappers with 'error-state' classes.
    ERROR_MESSAGE = (By.CSS_SELECTOR,
        "ul.errors, "
        "form[action*='/account/login'] .errors, "
        ".notice--error, "
        "[data-form-status]"
    )

    # Scoped to the login form specifically — prevents matching the search bar's
    # submit button, which also uses input[type='submit'] and caused tests to
    # navigate to /search?type=product&q= instead of submitting the login form.
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
        # Wait for the POST -> redirect -> page-load cycle to complete before
        # any subsequent assertions. Without this, has_error_message() starts
        # polling while the page is mid-reload and may miss the error element.
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
        Returns True when a visible, non-empty error message is present.

        Uses visibility_of_element_located (not presence_of_element_located) so
        that an empty or hidden .errors container — which Shopify may render in
        the DOM even on a clean page load — does not produce a false positive.
        The .text.strip() check provides a second guard: the element must also
        contain actual error copy, not just be visible.
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return bool(element.text.strip())
        except Exception:
            return False

    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)