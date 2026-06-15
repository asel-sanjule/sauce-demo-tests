from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CatalogPage(BasePage):
    """Page object for https://sauce-demo.myshopify.com/collections/all"""

    # ── Locators ──────────────────────────────────────────────────────────────
    # All product links follow the pattern /collections/all/products/<slug>
    # Using href-based XPath is far more reliable than CSS class names
    # which vary by Shopify theme version.

    PAGE_HEADING    = (By.CSS_SELECTOR, "h1")
    PRODUCT_LINKS   = (By.XPATH, "//a[contains(@href, '/collections/all/products/')]")
    SOLD_OUT_BADGES = (By.XPATH, "//*[contains(text(), 'Sold Out')]")

    # ── Actions ───────────────────────────────────────────────────────────────

    def open(self):
        return super().open("/collections/all")

    def get_all_products(self) -> list:
        return self.find_all(self.PRODUCT_LINKS)

    def get_product_titles(self) -> list[str]:
        """
        Returns visible text from each product link.
        Shopify product links contain both image alt text and title text,
        so the raw .text may look like 'Grey jacket Grey jacket £55.00'.
        The is_product_listed() check handles this via substring matching.
        """
        return [el.text.strip() for el in self.find_all(self.PRODUCT_LINKS) if el.text.strip()]

    def get_sold_out_items(self) -> list:
        return self.find_all(self.SOLD_OUT_BADGES)

    def click_product_by_text(self, product_name: str):
        """Click a product by partial name match."""
        self.click((By.PARTIAL_LINK_TEXT, product_name))

    # ── State checks ──────────────────────────────────────────────────────────

    def product_count(self) -> int:
        """Count distinct product links by unique href."""
        elements = self.get_all_products()
        unique_hrefs = set(el.get_attribute("href") for el in elements)
        return len(unique_hrefs)

    def sold_out_count(self) -> int:
        return len(self.get_sold_out_items())

    def is_product_listed(self, product_name: str) -> bool:
        titles = self.get_product_titles()
        return any(product_name.lower() in t.lower() for t in titles)