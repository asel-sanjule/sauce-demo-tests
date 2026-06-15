from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page object for https://sauce-demo.myshopify.com/cart"""

    # ── Locators ──────────────────────────────────────────────────────────────
    # Confirmed from live page:
    # Empty cart message text: "It appears that your cart is currently empty!"
    # Continue Shopping link:  "Continue Shopping" → /collections/all

    PAGE_HEADING       = (By.CSS_SELECTOR, "h1")
    EMPTY_CART_MESSAGE = (By.XPATH, "//*[contains(text(), 'currently empty')]")
    CONTINUE_SHOPPING  = (By.LINK_TEXT, "Continue Shopping")
    CART_ITEMS         = (By.CSS_SELECTOR, ".cart__item, .cart-item, tr.cart-item")
    CHECKOUT_BUTTON    = (By.CSS_SELECTOR, "input[name='checkout'], button[name='checkout']")

    # ── Actions ───────────────────────────────────────────────────────────────

    def open(self):
        return super().open("/cart")

    # ── State checks ──────────────────────────────────────────────────────────

    def is_cart_empty(self) -> bool:
        return self.is_visible(self.EMPTY_CART_MESSAGE)

    def is_continue_shopping_link_visible(self) -> bool:
        return self.is_visible(self.CONTINUE_SHOPPING)

    def get_empty_cart_text(self) -> str:
        return self.get_text(self.EMPTY_CART_MESSAGE)

    def cart_item_count(self) -> int:
        try:
            return len(self.find_all(self.CART_ITEMS))
        except Exception:
            return 0