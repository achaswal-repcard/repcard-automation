import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class LoginPage:

    def __init__(self, page):
        self.page = page

        # locators
        self.username_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.login_button = "button[type='submit']"
        # error banner text on invalid credentials
        self.error_message = "text=These credentials do not match our records."
        self.forgot_password_link = "a:has-text('Forgot password')"
        self.create_account = "a:has-text('Create account')"

    def enter_username(self, username):
        self.page.fill(self.username_input, username)

    def enter_password(self, password):
        self.page.fill(self.password_input, password)

    def click_login(self):
        self.page.click(self.login_button)

    def login(self, username, password):
        if username != "<empty>":
            self.enter_username(username)
        if password != "<empty>":
            self.enter_password(password)
        self.click_login()

    def is_error_displayed(self):
        return self.page.locator(self.error_message).is_visible()

    def _get_validation_message(self, selector):
        locator = self.page.locator(selector)
        if locator.count() == 0:
            return ""
        return locator.evaluate("el => el.validationMessage")

    def verify_login_success(self):
        # Successful login redirects to /admin/home
        self.page.wait_for_url("**/admin/home", timeout=10000)
        assert "/admin/home" in self.page.url
        with allure.step("Login successful: redirected to /admin/home"):
            pass

    def verify_login_error(self):
        # Unsuccessful login either shows a server error banner or native validation
        banner_visible = False
        try:
            self.page.locator(self.error_message).wait_for(state="visible", timeout=5000)
            banner_visible = True
        except PlaywrightTimeoutError:
            banner_visible = False

        username_validation = self._get_validation_message(self.username_input)
        password_validation = self._get_validation_message(self.password_input)

        assert (
            banner_visible or username_validation or password_validation
        ), "Login unsuccessful: no error banner or validation message found"

        with allure.step("Login unsuccessful: error message displayed"):
            pass

    def click_forgot_password(self):
        self.page.locator(self.forgot_password_link).click()

    def click_create_account(self):
         self.page.locator(self.create_account).click()
