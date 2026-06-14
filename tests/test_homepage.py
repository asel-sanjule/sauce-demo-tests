import pytest
from pages.home_page import HomePage


class TestHomePage:
    """
    Validates the homepage loads correctly with the expected content.
    These are smoke-level checks — fast, no deep interaction.
    """

    @pytest.mark.smoke
    def test_page_title_is_correct(self, home_driver):
        page = HomePage(home_driver)
        assert "Sauce Demo" in page.title(), (
            f"Expected 'Sauce Demo' in title, got: '{page.title()}'"
        )

    @pytest.mark.smoke
    def test_site_heading_is_visible(self, home_driver):
        page = HomePage(home_driver)
        assert page.is_site_heading_visible(), "Site heading <h1> should be visible on homepage"

    @pytest.mark.smoke
    def test_homepage_url_is_correct(self, home_driver):
        page = HomePage(home_driver)
        assert "sauce-demo.myshopify.com" in page.current_url()

    @pytest.mark.regression
    def test_login_link_is_present_in_nav(self, home_driver):
        page = HomePage(home_driver)
        assert page.is_login_link_present(), "Login link should be visible in nav"

    @pytest.mark.regression
    def test_cart_link_is_present_in_nav(self, home_driver):
        page = HomePage(home_driver)
        assert page.is_cart_link_present(), "Cart link should be visible in nav"

    @pytest.mark.regression
    def test_featured_products_are_displayed(self, home_driver):
        page = HomePage(home_driver)
        count = page.featured_product_count()
        assert count > 0, f"Expected at least 1 featured product on homepage, found {count}"

    @pytest.mark.regression
    def test_homepage_has_three_featured_products(self, home_driver):
        page = HomePage(home_driver)
        count = page.featured_product_count()
        assert count == 3, f"Expected 3 featured products, found {count}"
