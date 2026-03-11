import time
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, expect


class CalendarPage:
    def __init__(self, page):
        self.page = page
        self.calendar_name_input = "#calendar_name, #calendarName"
        self.calendar_description_input = "#calendar_desc, textarea[name='description']"
        self.external_calendar_name_input = "#external_calendar_name, #externalCalendarName"
        self.external_calendar_description_input = "#external_calendar_desc"

    def open_create_calendar_page(self, base_url):
        self.page.goto(f"{base_url}/admin/calendar/create-calendar-new", wait_until="domcontentloaded")
        self.page.wait_for_url("**/admin/calendar/create-calendar-new*", timeout=15000)
        self._wait_for_page_stable()
        assert "/admin/calendar/create-calendar-new" in self.page.url

    def select_direct_assign(self):
        direct_assign = self.page.locator(".for-directassing, :text('Direct Assign')").first
        expect(direct_assign).to_be_visible(timeout=15000)
        direct_assign.click()
        self._wait_for_page_stable()

    def select_dispatcher(self):
        dispatcher = self.page.locator(".for-dispatcher, :text('Dispatcher')").first
        expect(dispatcher).to_be_visible(timeout=15000)
        dispatcher.click()
        self._wait_for_page_stable()

    def select_dispatcher_checkbox_and_continue(self):
        """
        Dispatcher flow requires selecting Setter, Closer, and Dispatcher
        before next.
        """
        self.wait_for_users_list_populated()

        # Variant 1: legacy DOM has explicit data-checkbox-type.
        role_types = ["setter", "closer", "dispatcher"]
        legacy_any = False
        for role in role_types:
            checkbox = self.page.locator(f"input[data-checkbox-type='{role}']").first
            if checkbox.count() > 0 and checkbox.is_visible():
                legacy_any = True
                if not checkbox.is_checked():
                    checkbox.check()
        if legacy_any:
            self._wait_for_page_stable()
            return

        # Variant 2: column-based grid/table. Click first row cells under
        # Setter/Closer/Dispatcher if they are unchecked.
        try:
            headers = self.page.locator("th:visible")
            role_index = {}
            for idx in range(headers.count()):
                text = headers.nth(idx).inner_text().strip().lower()
                if "setter" in text:
                    role_index["setter"] = idx
                elif "closer" in text:
                    role_index["closer"] = idx
                elif "dispatcher" in text:
                    role_index["dispatcher"] = idx

            rows = self.page.locator("table tbody tr:visible")
            if rows.count() > 0 and len(role_index) == 3:
                row = rows.first
                for role in role_types:
                    cell = row.locator("td").nth(role_index[role])
                    checked_icon = cell.locator("img[alt='Checked'], img[aria-label='Checked']")
                    if checked_icon.count() > 0 and checked_icon.first.is_visible():
                        continue
                    checkbox = cell.locator("input[type='checkbox'], [role='checkbox']").first
                    if checkbox.count() > 0 and checkbox.is_visible():
                        try:
                            if hasattr(checkbox, "is_checked") and checkbox.is_checked():
                                continue
                        except Exception:
                            pass
                        try:
                            checkbox.check()
                        except Exception:
                            checkbox.click()
                    else:
                        cell.click()
                self._wait_for_page_stable()
                return
        except Exception:
            pass

        # Variant 3: icon-based checkbox. Select 3 roles from row.
        unchecked = self.page.get_by_role("img", name="Unchecked")
        expect(unchecked.first).to_be_visible(timeout=20000)
        clicks = min(3, unchecked.count())
        for i in range(clicks):
            unchecked.nth(i).click()
        self._wait_for_page_stable()

    def fill_basic_details(self, calendar_name, description):
        calendar_name_field = self.page.locator(self.calendar_name_input)
        description_field = self.page.locator(self.calendar_description_input)
        expect(calendar_name_field).to_be_visible(timeout=15000)
        expect(description_field).to_be_visible(timeout=15000)
        calendar_name_field.first.fill(calendar_name)
        description_field.first.fill(description)
        self._wait_for_page_stable()

    def click_next(self):
        next_btn = self.page.locator("a:has-text('Next'), button:has-text('Next')").last
        expect(next_btn).to_be_visible(timeout=15000)
        next_btn.click()
        self._wait_for_page_stable()

    def select_first_two_participants(self):
        self.wait_for_users_list_populated()
        unchecked = self.page.get_by_role("img", name="Unchecked")
        selected = 0
        while selected < 2:
            count = unchecked.count()
            if count == 0:
                break
            unchecked.first.click()
            selected += 1
            self.page.wait_for_timeout(250)
        self._wait_for_page_stable()

    def wait_for_users_list_populated(self):
        """
        On the Add Users step, wait until selectable user rows are rendered.
        """
        selectors = [
            self.page.locator("input[data-checkbox-type='dispatcher']").first,
            self.page.locator("input[data-checkbox-type='setter']").first,
            self.page.get_by_role("img", name="Unchecked").first,
            self.page.locator("table tbody tr:visible").first,
        ]
        for locator in selectors:
            try:
                expect(locator).to_be_visible(timeout=5000)
                self._wait_for_page_stable()
                return
            except Exception:
                continue

        raise AssertionError("Add Users list did not become ready.")

    def move_to_final_step(self, max_next_clicks=15):
        for _ in range(max_next_clicks):
            if self._is_external_step_ready() or self._submit_button().is_visible():
                return
            next_btn = self._next_button()
            if not next_btn.is_visible():
                return
            self.click_next()
            self._wait_for_page_stable()

    def fill_external_calendar_details_if_visible(self, calendar_name, description):
        field = self.page.locator(self.external_calendar_name_input)
        if field.count() > 0 and field.first.is_visible():
            field.first.fill(calendar_name)
            external_desc = self.page.locator(self.external_calendar_description_input)
            if external_desc.count() > 0 and external_desc.first.is_visible():
                external_desc.first.fill(description)
            self._wait_for_page_stable()

    def configure_availability_settings(self):
        """
        Availability step selections before moving to next section.
        This keeps defaults stable but explicitly selects key controls.
        """
        # Wait for Availability step content.
        availability_markers = [
            self.page.get_by_text("Availability"),
            self.page.get_by_text("Booking Flow"),
            self.page.get_by_text("Calendar Date Range"),
        ]
        marker_seen = False
        for marker in availability_markers:
            try:
                expect(marker.first).to_be_visible(timeout=5000)
                marker_seen = True
                break
            except Exception:
                continue
        if not marker_seen:
            raise AssertionError("Availability section did not load.")

        # Checkbox option: allow timezone change.
        can_change_timezone = self.page.locator("#can_change_timezone").first
        if can_change_timezone.count() > 0 and can_change_timezone.is_visible():
            if not can_change_timezone.is_checked():
                can_change_timezone.check()

        # Radio option: booking flow selection.
        booking_flow = self.page.locator("input[name='booking-style'][value='0']").first
        if booking_flow.count() > 0 and booking_flow.is_visible():
            booking_flow.check()

        # Radio option: no date range limit.
        no_date_limit = self.page.locator("input[name='range-type'][value='3']").first
        if no_date_limit.count() > 0 and no_date_limit.is_visible():
            no_date_limit.check()

        # Availability hours: ensure at least one day is enabled.
        monday_toggle = self.page.locator("#chk2").first
        if monday_toggle.count() > 0 and monday_toggle.is_visible() and not monday_toggle.is_checked():
            monday_toggle.check()

        # Dropdown option (if select exists in current variant).
        timezone_select = self.page.locator("select#time_zone, select[name='time_zone']").first
        if timezone_select.count() > 0 and timezone_select.is_visible():
            try:
                timezone_select.select_option(index=1)
            except Exception:
                pass

        # Required in some variants to avoid 422 for calendarAvailableHours.
        self._set_booking_availability_if_present()

        self._wait_for_page_stable()

    def submit_create_calendar_and_capture_api(self):
        self._set_booking_availability_if_present()
        submit_btn = self._submit_button()
        expect(submit_btn).to_be_visible(timeout=15000)
        self._wait_for_page_stable()  # Ensure page is fully ready before clicking
        
        retry_count = 0
        while retry_count < 3:
            try:
                with self.page.expect_response(
                    lambda r: r.request.method == "POST" and "/api/v1/calendars" in r.url,
                    timeout=25000,
                ) as response_info:
                    submit_btn.click()
                response = response_info.value
                try:
                    response_body = response.text()
                except Exception:
                    response_body = "{\"info\": \"response body unavailable\"}"
                return response.status, response_body
            except PlaywrightTimeoutError:
                retry_count += 1
                if retry_count >= 3:
                    raise
                self.page.wait_for_timeout(500)

    @staticmethod
    def build_unique_calendar_name(prefix="Calendar-auto"):
        return f"{prefix}-{int(time.time())}"

    def assert_on_create_page(self):
        selectors = [
            self.page.get_by_text("Select calendar type"),
            self.page.get_by_text("Create new calendar"),
            self.page.get_by_text("Direct Assign"),
            self.page.get_by_role("button", name="Direct Assign Direct Assign"),
        ]
        for locator in selectors:
            try:
                expect(locator.first).to_be_visible(timeout=4000)
                return
            except Exception:
                continue
        raise AssertionError("Calendar create page did not load expected calendar type UI.")

    def _submit_button(self):
        return self.page.locator(
            "button:has-text('Create Calendar'), "
            "a:has-text('Create Calendar'), "
            "a.submit-calendar, "
            "a.add-calendar-button, "
            "button:has-text('Save'), "
            "a:has-text('Save')"
        ).last

    def _next_button(self):
        return self.page.locator(
            "a.next:visible, "
            "button:has-text('Next'):visible, "
            "a:has-text('Next'):visible"
        ).last

    def _is_external_step_ready(self):
        field = self.page.locator(self.external_calendar_name_input).first
        return field.count() > 0 and field.is_visible()

    def _select_calendar_type(self, button_name):
        calendar_type_btn = self.page.get_by_role("button", name=button_name)
        expect(calendar_type_btn).to_be_visible(timeout=15000)
        calendar_type_btn.click()
        self._wait_for_page_stable()

    def _wait_for_page_stable(self):
        # Move ahead as soon as the next step is interactable.
        self.page.wait_for_load_state("domcontentloaded")
        try:
            self.page.wait_for_load_state("networkidle", timeout=3000)
        except PlaywrightTimeoutError:
            pass
        self.page.wait_for_timeout(500)

    def _set_booking_availability_if_present(self):
        hour_inputs = self.page.locator("input[name*='calendarAvailableHours']")
        if hour_inputs.count() == 0:
            return
        for idx in range(hour_inputs.count()):
            option = hour_inputs.nth(idx)
            if not option.is_visible():
                continue
            try:
                if option.is_checked():
                    return
            except Exception:
                pass
            try:
                option.check()
            except Exception:
                option.click()
            return
