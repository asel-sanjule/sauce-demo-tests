import pytest
from pages.home_page import HomePage

BASE_URL = "https://sauce-demo.myshopify.com"


class TestNavigation:
    """
    Verifies that all primary navigation links route to the correct pages.
    Each test starts fresh from the homepage.
    """

    @pytest.mark.smoke
    @pytest.mark.navigation
    def test_catalog_nav_link_goes_to_correct_url(self, home_driver):
        page = HomePage(home_driver)
        page.click_catalog_nav()
        assert home_driver.current_url == BASE_URL + "/collections/all", (
            f"Expected catalog URL, got: {home_driver.current_url}"
        )

    @pytest.mark.navigation
    def test_login_nav_link_goes_to_correct_url(self, home_driver):
        page = HomePage(home_driver)
        page.click_login_nav()
        assert "/account/login" in home_driver.current_url

    @pytest.mark.navigation
    def test_signup_nav_link_goes_to_correct_url(self, home_driver):
        page = HomePage(home_driver)
        page.click_signup_nav()
        assert "/account/register" in home_driver.current_url

    @pytest.mark.navigation
    def test_cart_nav_link_goes_to_correct_url(self, home_driver):
        page = HomePage(home_driver)
        page.click_cart_nav()
        assert "/cart" in home_driver.current_url

    @pytest.mark.navigation
    def test_browser_back_returns_to_homepage(self, home_driver):
        page = HomePage(home_driver)
        page.click_catalog_nav()
        home_driver.back()
        assert "sauce-demo.myshopify.com" in home_driver.current_url
