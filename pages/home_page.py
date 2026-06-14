from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for https://sauce-demo.myshopify.com/"""

    # ── Locators ─────────────────────────────────────────────────────────────
    # Using href-based CSS selectors for nav links — the most stable
    # locator strategy for anchor tags on any site.

    SITE_HEADING     = (By.CSS_SELECTOR, "h1 a")
    NAV_CATALOG      = (By.CSS_SELECTOR, "a[href='/collections/all']")
    NAV_LOGIN        = (By.CSS_SELECTOR, "a[href='/account/login']")
    NAV_SIGNUP       = (By.CSS_SELECTOR, "a[href='/account/register']")
    NAV_CART         = (By.CSS_SELECTOR, "a[href='/cart']")
    NAV_SEARCH       = (By.CSS_SELECTOR, "a[href='/search']")
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, "#frontpage-article .grid__item")

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
        self.click(self.NAV_CART)

    # ── State checks ──────────────────────────────────────────────────────────

    def is_site_heading_visible(self) -> bool:
        return self.is_visible(self.SITE_HEADING)

    def is_login_link_present(self) -> bool:
        return self.is_visible(self.NAV_LOGIN)

    def is_cart_link_present(self) -> bool:
        return self.is_visible(self.NAV_CART)

    def featured_product_count(self) -> int:
        return len(self.get_featured_products())
