import pytest
from pages.catalog_page import CatalogPage


class TestCatalog:
    """
    Validates the product catalog (/collections/all).
    Covers product count, sold-out state, and specific product presence.
    """

    # Expected products from site inspection
    EXPECTED_PRODUCTS = [
        "Black heels",
        "Bronze sandals",
        "Brown Shades",
        "Grey jacket",
        "Noir jacket",
        "Striped top",
        "White sandals",
    ]
    EXPECTED_SOLD_OUT = ["Brown Shades", "White sandals"]

    @pytest.mark.smoke
    @pytest.mark.catalog
    def test_catalog_page_title_contains_products(self, catalog_driver):
        page = CatalogPage(catalog_driver)
        assert "Products" in page.title()

    @pytest.mark.smoke
    @pytest.mark.catalog
    def test_catalog_url_is_correct(self, catalog_driver):
        assert "/collections/all" in catalog_driver.current_url

    @pytest.mark.regression
    @pytest.mark.catalog
    def test_catalog_displays_all_seven_products(self, catalog_driver):
        page = CatalogPage(catalog_driver)
        count = page.product_count()
        assert count == 7, f"Expected 7 products, found {count}"

    @pytest.mark.regression
    @pytest.mark.catalog
    def test_two_products_are_marked_sold_out(self, catalog_driver):
        page = CatalogPage(catalog_driver)
        count = page.sold_out_count()
        assert count == 2, f"Expected 2 sold-out products, found {count}"

    @pytest.mark.regression
    @pytest.mark.catalog
    @pytest.mark.parametrize("product_name", EXPECTED_PRODUCTS)
    def test_expected_product_is_listed(self, catalog_driver, product_name):
        """Parametrized: runs once per product name in EXPECTED_PRODUCTS."""
        page = CatalogPage(catalog_driver)
        assert page.is_product_listed(product_name), (
            f"Product '{product_name}' was not found in catalog"
        )

    @pytest.mark.regression
    @pytest.mark.catalog
    def test_clicking_product_navigates_to_product_page(self, catalog_driver):
        page = CatalogPage(catalog_driver)
        page.click_product_by_text("Grey jacket")
        assert "/products/grey-jacket" in catalog_driver.current_url
