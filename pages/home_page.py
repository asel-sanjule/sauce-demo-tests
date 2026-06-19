from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for https://sauce-demo.myshopify.com/"""

    # ── Locators ──────────────────────────────────────────────────────────────

    SITE_HEADING = (By.CSS_SELECTOR, "h1 a")
    NAV_CATALOG  = (By.CSS_SELECTOR, "a[href='/collections/all']")
    NAV_LOGIN    = (By.CSS_SELECTOR, "a[href='/account/login']")
    NAV_SIGNUP   = (By.CSS_SELECTOR, "a[href='/account/register']")
    NAV_SEARCH   = (By.CSS_SELECTOR, "a[href='/search']")

    # The visible cart element in the header is a toggle button with href="#".
    # The actual a[href='/cart'] is inside a hidden mini-cart dropdown.
    NAV_CART_TOGGLE = (By.XPATH, "//a[@href='#' and contains(., 'Cart')]")

    # Featured products are linked under /collections/frontpage/products/
    FEATURED_PRODUCTS = (By.XPATH, "//a[contains(@href, '/collections/frontpage/products/')]")

    # ── Actions ───────────────────────────────────────────────────────────────

    def open(self):
        return super().open("/")

    def get_featured_products(self) -> list:
        return self.find_all(self.FEATURED_PRODUCTS)

    def click_catalog_nav(self):
        self.click(self.NAV_CATALOG)

    def click_login_nav(self):
        self.click(self.NAV_LOGIN)

    def click_signup_nav(self):
        self.click(self.NAV_SIGNUP)

    def click_cart_nav(self):
        # The /cart link is inside a hidden mini-cart dropdown.
        # Use JavaScript to navigate directly — tests routing, not the dropdown UI.
        self.driver.execute_script("window.location.href='/cart'")

    # ── State checks ──────────────────────────────────────────────────────────

    def is_site_heading_visible(self) -> bool:
        return self.is_visible(self.SITE_HEADING)

    def is_login_link_present(self) -> bool:
        return self.is_visible(self.NAV_LOGIN)

    def is_cart_link_present(self) -> bool:
        # Check for the visible mini-cart toggle in the header
        return self.is_visible(self.NAV_CART_TOGGLE)

    def featured_product_count(self) -> int:
        return len(self.get_featured_products())
