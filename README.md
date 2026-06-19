# Sauce Demo — Selenium + Pytest Automation Suite

![Regression Suite](https://github.com/asel-sanjule/sauce-demo-tests/actions/workflows/regression.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4.18-green?logo=selenium)
![Pytest](https://img.shields.io/badge/Pytest-8.1-orange)

End-to-end regression suite for [sauce-demo.myshopify.com](https://sauce-demo.myshopify.com) — a Shopify demo storefront.
Built with **Python**, **Selenium WebDriver**, and **Pytest**, integrated into a **GitHub Actions CI pipeline**.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.11 |
| Browser automation | Selenium WebDriver 4.18 |
| Test framework | Pytest 8.1 |
| Driver management | webdriver-manager (auto-installs ChromeDriver) |
| Reporting | pytest-html (self-contained HTML report) |
| CI/CD | GitHub Actions |

---

## Coverage

| Module | Tests | Markers |
|---|---|---|
| Homepage | 7 | `smoke`, `regression` |
| Navigation | 5 | `smoke`, `navigation` |
| Product Catalog | 12 | `smoke`, `regression`, `catalog` |
| Login Page | 8 | `smoke`, `regression`, `login` |
| Cart | 6 | `smoke`, `regression`, `cart` |
| **Total** | **38** | |

---

## Project Structure

```
sauce-demo-tests/
├── .github/
│   └── workflows/
│       └── regression.yml   ← CI pipeline (runs on every push to main)
├── conftest.py               ← Shared fixtures: driver setup, pre-navigated sessions
├── pytest.ini                ← Markers, report config
├── requirements.txt
├── pages/                    ← Page Object Model
│   ├── base_page.py          ← Shared wait utilities and action wrappers
│   ├── home_page.py
│   ├── catalog_page.py
│   ├── login_page.py
│   └── cart_page.py
└── tests/
    ├── test_homepage.py
    ├── test_navigation.py
    ├── test_catalog.py
    ├── test_login.py
    └── test_cart.py
```

---

## Setup

```bash
# Clone the repo
git clone https://github.com/asel-sanjule/sauce-demo-tests.git
cd sauce-demo-tests

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows

# Install dependencies (ChromeDriver auto-managed)
pip install -r requirements.txt
```

---

## Running Tests

```bash
# Full suite
pytest

# Smoke tests only (fast, ~10 tests)
pytest -m smoke

# By feature area
pytest -m catalog
pytest -m login
pytest -m navigation

# Single test file
pytest tests/test_catalog.py -v

# Single test
pytest tests/test_catalog.py::TestCatalog::test_catalog_displays_all_seven_products
```

> **Headless by default.** To run with a visible browser, remove `--headless`
> from `build_driver()` in `conftest.py`.

---

## HTML Report

Every run generates `reports/regression-report.html`.
In CI, the report is uploaded as a downloadable artifact under **Actions → Run → Artifacts**.

---

## Design Decisions

**Page Object Model** — Each page has its own class under `pages/`. Locators are defined as class-level tuples, not scattered through test files. A selector change requires updating one place.

**Pre-navigated fixtures** — `conftest.py` provides `home_driver`, `catalog_driver`, `login_driver`, and `cart_driver`. Tests receive a browser already on the right page, keeping test methods focused on behaviour rather than setup.

**Explicit waits throughout** — `BasePage` uses `WebDriverWait` with `expected_conditions` for all element interactions. No `time.sleep()` calls.

**Pytest markers** — Tests are tagged `smoke` or `regression` (and a feature tag). The CI pipeline runs smoke first, then the full suite, so a fast failure is surfaced early.

**Parametrized catalog test** — `test_expected_product_is_listed` runs once per product using `@pytest.mark.parametrize`, producing individual pass/fail per product name in the report.
