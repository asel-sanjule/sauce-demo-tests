from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

BASE_URL = "https://sauce-demo.myshopify.com"


class BasePage:
    """
    All page objects inherit from this class.
    It wraps Selenium's raw WebDriver calls behind clean, readable methods —
    the same intent as Playwright's built-in page.locator(), expect(), etc.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ── Navigation ──────────────────────────────────────────────────────────

    def open(self, path: str = ""):
        self.driver.get(BASE_URL + path)
        return self

    def current_url(self) -> str:
        return self.driver.current_url

    def title(self) -> str:
        return self.driver.title

    # ── Element retrieval ───────────────────────────────────────────────────
    # Equivalent to Playwright's page.locator() — waits up to 10s before failing.

    def find(self, locator: tuple):
        """Wait for a single element to be present in the DOM."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: tuple) -> list:
        """Wait for at least one matching element, return all matches."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def find_clickable(self, locator: tuple):
        """Wait for an element to be visible and enabled."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    # ── Actions ─────────────────────────────────────────────────────────────

    def click(self, locator: tuple):
        """Equivalent to Playwright's locator.click()."""
        self.find_clickable(locator).click()

    def type_text(self, locator: tuple, text: str):
        """Equivalent to Playwright's locator.fill()."""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def wait_for_page_load(self, timeout: int = 15):
        """
        Blocks until the browser reports document.readyState == 'complete'.
        Call this after any action that triggers a full page navigation (form
        submit, link click) so subsequent assertions don't race the reload.
        Equivalent to Playwright's page.wait_for_load_state('load').
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except Exception:
            pass  # Best-effort — don't crash the test if the hook times out

    # ── Assertions helpers ───────────────────────────────────────────────────
    # Playwright has expect(locator).toBeVisible() — here we use is_displayed().
    # These helpers keep test files clean and readable.

    def is_visible(self, locator: tuple) -> bool:
        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except Exception:
            return False

    def get_text(self, locator: tuple) -> str:
        return self.find(locator).text.strip()