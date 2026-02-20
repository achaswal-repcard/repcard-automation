class ForgotPasswordPage:
    def __init__(self, page):
        self.page = page

        # Input & button
        self.email_input = 'input[name="email"]'
        self.reset_password_button = 'button[type="submit"]'

        # Messages (adjust selector if UI changes)
        self.success_message = "div.alert.alert-success, div.alert-success"
        # Try common error patterns: red text, alerts, or error keywords
        self.error_message_selectors = [
            "span.help-block strong",
            "span.help-block",
            '[role="alert"]',
            "div.alert-danger",
            "div.alert-error",
            "text=/can.t find a user|valid email|not found|error/i",
        ]

    def enter_email(self, email):
        self.page.fill(self.email_input, email)

    def click_reset_password(self):
        self.page.click(self.reset_password_button)

    def is_success_message_displayed(self):
        return self.page.locator(self.success_message).first.is_visible()

    def is_error_message_displayed(self):
        return self._get_error_locator().is_visible()

    def get_success_message_text(self):
        return self.page.locator(self.success_message).first.inner_text()

    def get_error_message_text(self):
        return self._get_error_locator().inner_text()

    def _get_error_locator(self):
        for selector in self.error_message_selectors:
            locator = self.page.locator(selector).first
            try:
                locator.wait_for(state="visible", timeout=2000)
                return locator
            except Exception:
                continue
        return self.page.locator(self.error_message_selectors[0]).first
