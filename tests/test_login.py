import pytest
from pages.login_page import LoginPage


class TestLoginPage:
    """
    Validates the login page structure and form behaviour.
    Does not test a successful login — no valid credentials are available
    for this demo store. Invalid-credential testing verifies the error
    handling path, which is a valid and important test case.
    """

    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_page_title_is_correct(self, login_driver):
        page = LoginPage(login_driver)
        assert "Account" in page.title() or "Login" in page.title()

    @pytest.mark.smoke
    @pytest.mark.login
    def test_email_field_is_present(self, login_driver):
        page = LoginPage(login_driver)
        assert page.is_email_field_present(), "Email input should be visible on login page"

    @pytest.mark.smoke
    @pytest.mark.login
    def test_password_field_is_present(self, login_driver):
        page = LoginPage(login_driver)
        assert page.is_password_field_present(), "Password input should be visible on login page"

    @pytest.mark.smoke
    @pytest.mark.login
    def test_submit_button_is_present(self, login_driver):
        page = LoginPage(login_driver)
        assert page.is_submit_button_present(), "Submit button should be visible on login page"

    @pytest.mark.regression
    @pytest.mark.login
    def test_forgot_password_link_is_present(self, login_driver):
        page = LoginPage(login_driver)
        assert page.is_forgot_password_link_present(), "'Forgot your password?' link should be present"

    @pytest.mark.regression
    @pytest.mark.login
    def test_login_url_is_correct(self, login_driver):
        assert "/account/login" in login_driver.current_url

    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_credentials_show_error(self, login_driver):
        """
        Attempting login with bad credentials should display an error.
        This validates the negative path — an important QA concern.
        """
        page = LoginPage(login_driver)
        page.attempt_login("invalid@test.com", "wrongpassword")
        assert page.has_error_message(), (
            "An error message should appear after submitting invalid credentials"
        )

    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_form_submission_stays_on_login_page(self, login_driver):
        """Submitting empty form should not navigate away from login page."""
        page = LoginPage(login_driver)
        page.click_submit()
        assert "/account/login" in page.current_url()
