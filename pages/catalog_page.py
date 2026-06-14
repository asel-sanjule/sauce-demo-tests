from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CatalogPage(BasePage):
    """Page object for https://sauce-demo.myshopify.com/collections/all"""

    # ── Locators ──────────────────────────────────────────────────────────────

    PAGE_HEADING     = (By.CSS_SELECTOR, "h1")
    PRODUCT_ITEMS    = (By.CSS_SELECTOR, ".grid__item")
    PRODUCT_TITLES   = (By.CSS_SELECTOR, ".grid__item .product-title, .grid__item h3")
    PRODUCT_PRICES   = (By.CSS_SELECTOR, ".grid__item .price, .grid__item .product-price")
    SOLD_OUT_BADGES  = (By.XPATH, "//*[contains(text(), 'Sold Out')]")

    # ── Actions ───────────────────────────────────────────────────────────────

    def open(self):
        return super().open("/collections/all")

    def get_all_products(self) -> list:
        return self.find_all(self.PRODUCT_ITEMS)

    def get_product_titles(self) -> list[str]:
        return [el.text.strip() for el in self.find_all(self.PRODUCT_TITLES) if el.text.strip()]

    def get_sold_out_items(self) -> list:
        return self.find_all(self.SOLD_OUT_BADGES)

    def click_product_by_text(self, product_name: str):
        """Click on a product link by its visible name."""
        locator = (By.LINK_TEXT, product_name)
        self.click(locator)

    # ── State checks ──────────────────────────────────────────────────────────

    def product_count(self) -> int:
        return len(self.get_all_products())

    def sold_out_count(self) -> int:
        return len(self.get_sold_out_items())

    def is_product_listed(self, product_name: str) -> bool:
        titles = self.get_product_titles()
        return any(product_name.lower() in t.lower() for t in titles)
