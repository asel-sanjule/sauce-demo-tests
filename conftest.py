import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://sauce-demo.myshopify.com"


def build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    # Prevent Shopify's bot detection from flagging headless Chrome.
    # navigator.webdriver=true and the "enable-automation" switch are the
    # two signals most anti-bot systems check first.
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    # Patch navigator.webdriver at the JS level as a second layer of cover.
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    return driver


# ── Screenshot on failure ────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot whenever a test fails, uploaded as a CI artifact."""
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
    yield _driver
    _driver.quit()


# ── Pre-navigated convenience fixtures ──────────────────────────────────────

@pytest.fixture
def home_driver(driver):
    driver.get(BASE_URL + "/")
    return driver


@pytest.fixture
def catalog_driver(driver):
    driver.get(BASE_URL + "/collections/all")
    return driver


@pytest.fixture
def login_driver(driver):
    driver.get(BASE_URL + "/account/login")
    return driver


@pytest.fixture
def cart_driver(driver):
    driver.get(BASE_URL + "/cart")
    return driver
