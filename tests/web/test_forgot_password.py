import allure
from pytest_bdd import scenario, given, when, then, parsers
from pages.web.login_page import LoginPage
from pages.web.forgot_password_page import ForgotPasswordPage


# -------------------- Scenarios --------------------

@scenario(
    "forgot_password.feature",
    "Reset password with registered email"
)
def test_forgot_password_success():
    pass


@scenario(
    "forgot_password.feature",
    "Reset password with unregistered or invalid email"
)
def test_forgot_password_failure():
    pass


# -------------------- Steps --------------------

@given("the user is on the login page")
def user_on_login_page(page, config):
    page.goto(config["base_url"])


@when("the user clicks on Forgot Password link")
def click_forgot_password(page):
    LoginPage(page).click_forgot_password()


@when(parsers.parse('the user enters email "{email}"'))
def enter_email(page, email):
    ForgotPasswordPage(page).enter_email(email)


@when("the user clicks on Reset Password button")
def click_reset_password(page):
    ForgotPasswordPage(page).click_reset_password()


@then("a success message should be displayed")
def verify_success_message(page):
    forgot_page = ForgotPasswordPage(page)
    message = forgot_page.get_success_message_text()

    with allure.step("Verify success message text"):
        assert forgot_page.is_success_message_displayed()
        assert "password reset link" in message.lower()


@then("an error message should be displayed")
def verify_error_message(page):
    forgot_page = ForgotPasswordPage(page)
    message = forgot_page.get_error_message_text()
    message_lower = message.lower()

    with allure.step("Verify error message text"):
        assert forgot_page.is_error_message_displayed()
        assert (
            "valid email" in message_lower
            or "not found" in message_lower
            or "can't find a user" in message_lower
            or "cannot find a user" in message_lower
            or "e-mail address" in message_lower
        )
