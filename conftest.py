import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://sauce-demo.myshopify.com"


def build_driver() -> webdriver.Chrome:
    """
    Builds and returns a configured Chrome WebDriver instance.

    Selenium 4.6+ ships with selenium-manager, a built-in driver manager that
    automatically locates or downloads the correct ChromeDriver binary.
    No third-party webdriver-manager package needed.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")

    return webdriver.Chrome(options=options)


# ── Screenshot on failure ────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Save a screenshot whenever a test fails.
    Files land in screenshots/ and are uploaded as a CI artifact so you can
    see exactly what the browser was showing when the assertion failed.
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            safe_name = (
                rep.nodeid
                .replace("/", "_")
                .replace("::", "_")
                .replace("[", "_")
                .replace("]", "_")
            )
            driver.save_screenshot(f"screenshots/{safe_name}.png")


# ── Core driver fixture ──────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def driver():
    """Provides a clean browser session for each test. Quits after the test completes."""
    _driver = build_driver()
    # NOTE: implicitly_wait is intentionally NOT set here.
    # Mixing implicit + explicit (WebDriverWait) waits is a known anti-pattern:
    # each internal find_element() call blocks for the full implicit timeout before
    # raising NoSuchElementException, which exhausts the WebDriverWait budget on
    # the very first poll — leaving zero time for retries.
    # All waiting is handled explicitly in BasePage via WebDriverWait.
    yield _driver
    _driver.quit()


# ── Pre-navigated convenience fixtures ──────────────────────────────────────

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