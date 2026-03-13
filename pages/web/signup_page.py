from playwright.sync_api import expect


class SignUpPage:
    def __init__(self, page):
        self.page = page

        # shared
        self.sign_in_link = "a:has-text('Sign In'), a:has-text('SIGN IN')"
        self.next_button = "a[href='#next']:visible, [role='menuitem']:has-text('Next'):visible"
        self.back_button = "a[href='#previous'], [role='menuitem']:has-text('Back')"
        self.step_1_section = "#steps-uid-0-p-0"
        self.step_2_section = "#steps-uid-0-p-1"
        self.step_3_section = "#steps-uid-0-p-2"

        # step 1
        self.first_name = "#firstname"
        self.last_name = "#lastname"
        self.email = "#email"
        self.password = "#password"
        self.username = "#username"
        self.phone = "#phone"

        # step 2
        self.company_name = "#cName"
        self.industry_select_button = "button[data-id='industryId']"
        self.industry_menu_item = ".dropdown-menu.open .inner li a .text"
        self.title = "#title"
        self.website = "#website"

        # step 3
        self.bio = "#bio"
        self.promotional_sms_checkbox = "input[name='opted_for_promotional_messages']"
        self.captcha = "div.g-recaptcha, iframe[title='reCAPTCHA']"
        self.finish_button = "#register-button, a[href='#finish']"

    def is_signup_page_displayed(self):
        return "/register" in self.page.url

    def click_sign_in(self):
        self.page.locator(self.sign_in_link).first.click()

    def is_step_1_displayed(self):
        return self.page.locator(self.first_name).is_visible()

    def is_step_2_displayed(self):
        return self.page.locator(self.company_name).is_visible()

    def is_step_3_displayed(self):
        return self.page.locator(self.bio).is_visible()

    def fill_step_1(self, data):
        self.page.fill(self.first_name, data["first_name"])
        self.page.locator(self.first_name).press("Tab")
        self.page.fill(self.last_name, data["last_name"])
        self.page.locator(self.last_name).press("Tab")
        self.page.fill(self.email, data["email"])
        self.page.locator(self.email).press("Tab")
        self.page.fill(self.password, data["password"])
        self.page.locator(self.password).press("Tab")
        self.page.fill(self.username, data["username"])
        self.page.locator(self.username).press("Tab")
        self.page.fill(self.phone, data["phone"])
        self.page.locator(self.phone).press("Tab")

    def click_next(self):
        self.page.locator(self.next_button).first.click()

    def fill_step_2(self, data):
        self.page.fill(self.company_name, data["company_name"])
        self.page.locator(self.industry_select_button).click()
        self.page.locator(self.industry_menu_item, has_text=data["industry"]).first.click()
        self.page.fill(self.title, data["job_title"])
        self.page.fill(self.website, data["website"])

    def fill_step_3_details(self, data):
        self.page.fill(self.bio, data["bio"])
        if data.get("opt_in_marketing", False):
            checkbox = self.page.locator(self.promotional_sms_checkbox)
            if not checkbox.is_checked():
                checkbox.check()

    def assert_step_2_visible(self):
        expect(self.page.locator(self.step_2_section)).to_have_attribute("aria-hidden", "false")
        expect(self.page.locator(self.company_name)).to_be_visible()

    def assert_step_3_visible(self):
        expect(self.page.locator(self.step_3_section)).to_have_attribute("aria-hidden", "false")
        expect(self.page.locator(self.bio)).to_be_visible()

    def assert_step_1_visible(self):
        expect(self.page.locator(self.step_1_section)).to_have_attribute("aria-hidden", "false")
        expect(self.page.locator(self.first_name)).to_be_visible()

    def assert_captcha_visible(self):
        expect(self.page.locator(self.captcha).first).to_be_visible()
