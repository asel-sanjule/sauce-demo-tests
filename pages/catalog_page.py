from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CatalogPage(BasePage):
    """Page object for https://sauce-demo.myshopify.com/collections/all"""

    PRODUCT_LINKS   = (By.XPATH, "//a[contains(@href, '/collections/all/products/')]")
    SOLD_OUT_BADGES = (By.XPATH, "//*[contains(text(), 'Sold Out')]")

    def open(self):
        return super().open("/collections/all")

    def get_all_products(self) -> list:
        return self.find_all(self.PRODUCT_LINKS)

    def get_product_titles(self) -> list[str]:
        """
        Shopify themes often place the product name in a visually-hidden span
        inside the <a> tag. Selenium's .text skips hidden text, so we use
        get_attribute('textContent') which reads all DOM text regardless of
        CSS visibility — equivalent to JavaScript's element.textContent.
        """
        titles = []
        for el in self.find_all(self.PRODUCT_LINKS):
            text = el.get_attribute("textContent").strip()
            if text:
                titles.append(text)
        return titles

    def get_sold_out_items(self) -> list:
        return self.find_all(self.SOLD_OUT_BADGES)

    def click_product_by_text(self, product_name: str):
        self.click((By.PARTIAL_LINK_TEXT, product_name))

    def product_count(self) -> int:
        elements = self.get_all_products()
        unique_hrefs = set(el.get_attribute("href") for el in elements)
        return len(unique_hrefs)

    def sold_out_count(self) -> int:
        return len(self.get_sold_out_items())

    def is_product_listed(self, product_name: str) -> bool:
        titles = self.get_product_titles()
        return any(product_name.lower() in t.lower() for t in titles)