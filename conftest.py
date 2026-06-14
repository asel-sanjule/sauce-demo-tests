import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://sauce-demo.myshopify.com"


def build_driver() -> webdriver.Chrome:
    """Builds and returns a configured Chrome WebDriver instance."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )


# ── Core driver fixture ─────────────────────────────────────────────────────
# scope="function" means a fresh browser is spun up for every test.
# This is the same as Playwright's default behaviour — no shared state between tests.

@pytest.fixture(scope="function")
def driver():
    """Provides a clean browser session for each test. Quits after the test completes."""
    _driver = build_driver()
    _driver.implicitly_wait(10)
    yield _driver
    _driver.quit()


# ── Pre-navigated convenience fixtures ─────────────────────────────────────
# These are exactly like Playwright's fixtures that accept a `page` argument
# and call page.goto() before the test body runs.

@pytest.fixture
def home_driver(driver):
    """Driver pre-navigated to the homepage."""
    driver.get(BASE_URL + "/")
    return driver


@pytest.fixture
def catalog_driver(driver):
    """Driver pre-navigated to the product catalog."""
    driver.get(BASE_URL + "/collections/all")
    return driver


@pytest.fixture
def login_driver(driver):
    """Driver pre-navigated to the login page."""
    driver.get(BASE_URL + "/account/login")
    return driver


@pytest.fixture
def cart_driver(driver):
    """Driver pre-navigated to the cart page."""
    driver.get(BASE_URL + "/cart")
    return driver
