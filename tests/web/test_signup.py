from pytest_bdd import scenario, given, when, then
from playwright.sync_api import expect
from pages.web.login_page import LoginPage
from pages.web.signup_page import SignUpPage
from tests.web.testdata.signup_data import realistic_signup_data


@scenario(
    "signup.feature",
    "Navigate to Sign Up page from Login page"
)
def test_navigate_to_signup():
    pass


@scenario(
    "signup.feature",
    "Navigate back to Login page from Sign Up page"
)
def test_navigate_back_to_login():
    pass


@scenario(
    "signup.feature",
    "Complete signup details across all 3 pages up to captcha verification"
)
def test_signup_three_step_flow_upto_captcha():
    pass


@given("the user is on the login page")
def user_on_login_page(page, config):
    page.goto(f"{config['base_url']}/admin/login")


@when("the user clicks on Create account button")
def click_create_account(page):
    LoginPage(page).click_create_account()


@when("the user clicks on Sign In link on Sign Up page")
def click_sign_in(page):
    SignUpPage(page).click_sign_in()


@then("the Sign Up page should be displayed")
def verify_signup_page(page):
    assert SignUpPage(page).is_signup_page_displayed()


@then("the signup step 1 should be displayed")
def verify_signup_step_1(page):
    SignUpPage(page).assert_step_1_visible()


@when("the user enters valid signup details on step 1")
def fill_signup_step_1(page, realistic_signup_data):
    SignUpPage(page).fill_step_1(realistic_signup_data)


@when("the user proceeds to signup step 2")
def go_to_signup_step_2(page):
    signup_page = SignUpPage(page)
    signup_page.click_next()
    signup_page.assert_step_2_visible()


@when("the user enters valid signup details on step 2")
def fill_signup_step_2(page, realistic_signup_data):
    SignUpPage(page).fill_step_2(realistic_signup_data)


@when("the user proceeds to signup step 3")
def go_to_signup_step_3(page):
    signup_page = SignUpPage(page)
    signup_page.click_next()
    signup_page.assert_step_3_visible()


@when("the user enters signup details on step 3 except captcha")
def fill_signup_step_3_except_captcha(page, realistic_signup_data):
    SignUpPage(page).fill_step_3_details(realistic_signup_data)


@then("captcha should be displayed before finishing signup")
def verify_captcha_gate(page):
    SignUpPage(page).assert_captcha_visible()


@then("the Login page should be displayed")
def verify_login_page(page):
    # Strong login page validation
    page.wait_for_url("**/admin/login", timeout=10000)
    expect(page.locator("input[name='email']")).to_be_visible()
