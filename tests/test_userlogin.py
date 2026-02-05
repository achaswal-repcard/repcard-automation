import allure
from pytest_bdd import scenarios, given, when, then, parsers

from pages.login_page import LoginPage


# Link feature file
scenarios("../features/login.feature")

@given("the user is on the login page")
def open_login_page(page, config):
    page.goto(f"{config['base_url']}/admin/login")


@when(parsers.parse('the user enters username "{username}"'))
def enter_username(page, username):
    """
    Handles normal and <empty> username values
    """
    if username != "<empty>":
        LoginPage(page).enter_username(username)


@when(parsers.parse('the user enters password "{password}"'))
def enter_password(page, password):
    """
    Handles normal and <empty> password values
    """
    if password != "<empty>":
        LoginPage(page).enter_password(password)


@when("the user clicks the login button")
def click_login(page):
    LoginPage(page).click_login()

@then("the user should be redirected to the home page")
def verify_successful_login(page):
    """
    Successful login validation
    """
    LoginPage(page).verify_login_success()


@then("an error message should be displayed")
def verify_login_error(page):
    """
    Invalid / empty login validation
    """
    LoginPage(page).verify_login_error()
