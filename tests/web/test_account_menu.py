from pytest_bdd import given, parsers, scenario, then, when

from pages.web.home_page import HomePage
from pages.web.login_page import LoginPage


@scenario(
    "account_menu.feature",
    "Account menu links redirect correctly and logout works",
)
def test_account_menu_links_and_logout():
    pass


@given("the user is logged in to the home page with valid credentials")
def login_to_home_page(page, config, assert_page_healthy):
    response = page.goto(f"{config['base_url']}/admin/login")
    assert_page_healthy(page, response)
    login_page = LoginPage(page)
    login_page.enter_username("admin@repcard.com")
    login_page.enter_password("Repcard1$")
    login_page.click_login()
    login_page.verify_login_success()


@when("the user opens the account dropdown menu")
def open_account_dropdown(page):
    HomePage(page).open_account_menu()


@when(parsers.parse('the user selects "{menu_item}" from account dropdown'))
def select_account_menu_item(page, menu_item):
    HomePage(page).click_account_menu_item(menu_item)


@then(parsers.parse('the system should redirect to "{destination}" page'))
def verify_destination_redirect(page, destination):
    home_page = HomePage(page)
    destination_key = destination.strip().lower()

    if destination_key == "profile":
        home_page.verify_profile_page()
    elif destination_key == "profile settings":
        home_page.verify_profile_settings_page()
    elif destination_key == "change password":
        home_page.verify_change_password_page()
    else:
        raise AssertionError(f"Unsupported destination value: {destination}")


@when("the user navigates back to the admin home page")
def navigate_back_to_home(page, config):
    HomePage(page).go_to_home_page(config["base_url"])


@when("the user logs out from account dropdown")
def logout_from_account_dropdown(page):
    HomePage(page).click_account_menu_item("Log Out")


@then("the system should redirect to admin login page")
def verify_logout_redirect_to_login(page):
    HomePage(page).verify_logged_out_to_login_page()
