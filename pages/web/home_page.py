from playwright.sync_api import expect


class HomePage:
    def __init__(self, page):
        self.page = page
        self.account_menu_toggle = "li.dropdown.user.user-menu > a.dropdown-toggle"
        self.account_menu_items = "li.dropdown.user.user-menu ul.dropdown-menu a"

    def open_account_menu(self):
        self.page.locator(self.account_menu_toggle).click()
        expect(self.page.locator("li.dropdown.user.user-menu ul.dropdown-menu")).to_be_visible()

    def click_account_menu_item(self, item_text):
        self.page.locator(self.account_menu_items, has_text=item_text).first.click()

    def verify_home_page(self):
        self.page.wait_for_url("**/admin/home", timeout=10000)
        assert "/admin/home" in self.page.url

    def verify_profile_page(self):
        self.page.wait_for_url("**/admin/employee/*/edit", timeout=10000)
        assert "/admin/employee/" in self.page.url and "/edit" in self.page.url

    def verify_profile_settings_page(self):
        self.page.wait_for_url("**/admin/users/*/settings", timeout=10000)
        assert "/admin/users/" in self.page.url and "/settings" in self.page.url

    def verify_change_password_page(self):
        self.page.wait_for_url("**/admin/change-password", timeout=10000)
        assert "/admin/change-password" in self.page.url

    def verify_logged_out_to_login_page(self):
        self.page.wait_for_url("**/admin/login", timeout=10000)
        assert "/admin/login" in self.page.url

    def go_to_home_page(self, base_url):
        self.page.goto(f"{base_url}/admin/home")
        self.verify_home_page()
