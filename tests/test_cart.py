import pytest
from pages.cart_page import CartPage


class TestCart:
    """
    Validates the cart page (/cart) in its initial empty state.
    """

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_cart_page_title_is_correct(self, cart_driver):
        page = CartPage(cart_driver)
        assert "Cart" in page.title() or "Shopping" in page.title()

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_cart_url_is_correct(self, cart_driver):
        assert "/cart" in cart_driver.current_url

    @pytest.mark.regression
    @pytest.mark.cart
    def test_empty_cart_shows_empty_message(self, cart_driver):
        page = CartPage(cart_driver)
        assert page.is_cart_empty(), "An empty cart should display an empty-state message"

    @pytest.mark.regression
    @pytest.mark.cart
    def test_empty_cart_has_continue_shopping_link(self, cart_driver):
        page = CartPage(cart_driver)
        assert page.is_continue_shopping_link_visible(), (
            "'Continue Shopping' link should be present in empty cart"
        )

    @pytest.mark.regression
    @pytest.mark.cart
    def test_empty_cart_has_no_line_items(self, cart_driver):
        page = CartPage(cart_driver)
        assert page.cart_item_count() == 0, "Empty cart should have 0 line items"

    @pytest.mark.regression
    @pytest.mark.cart
    def test_continue_shopping_link_routes_to_catalog(self, cart_driver):
        page = CartPage(cart_driver)
        page.click(page.CONTINUE_SHOPPING)
        assert "/collections/all" in cart_driver.current_url
