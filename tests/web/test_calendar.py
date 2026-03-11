import allure
import pytest
from pytest_bdd import given, scenario, then, when

from pages.web.calendar_page import CalendarPage
from pages.web.login_page import LoginPage
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


@scenario(
    "calendar.feature",
    "Company user creates direct assign calendar with default settings",
)
def test_company_user_creates_calendar():
    pass


@scenario(
    "calendar.feature",
    "Company user creates dispatcher calendar calendar with default settings",
)
def test_company_user_creates_dispatcher_calendar():
    pass


@scenario(
    "calendar.feature",
    "Company user creates direct assign calendar with availability settings",
)
def test_company_user_creates_direct_assign_calendar_with_availability_settings():
    pass


@scenario(
    "calendar.feature",
    "Company user creates dispatcher calendar with availability settings",
)
def test_company_user_creates_dispatcher_calendar_with_availability_settings():
    pass


@pytest.fixture
def calendar_payload():
    calendar_name = CalendarPage.build_unique_calendar_name("Calendar-internal")
    external_calendar_name = CalendarPage.build_unique_calendar_name("Calendar-external")
    return {
        "internal_calendar_name": calendar_name,
        "external_calendar_name": external_calendar_name,
        "internal_description": "Internal calendar description for automation",
        "external_description": "External calendar description for automation",
    }


@pytest.fixture
def calendar_create_response():
    return {}


@given("the company user is logged in and on create calendar page")
def company_user_on_calendar_page(page, config, assert_page_healthy):
    response = page.goto(f"{config['base_url']}/admin/login", wait_until="domcontentloaded")
    assert_page_healthy(page, response)

    login_page = LoginPage(page)
    login_page.enter_username("ac@mailinator.com")
    login_page.enter_password("Test@123")
    login_page.click_login()
    page.wait_for_load_state("domcontentloaded")
    try:
        page.wait_for_load_state("networkidle", timeout=1500)
    except PlaywrightTimeoutError:
        pass

    calendar_page = CalendarPage(page)
    calendar_page.open_create_calendar_page(config["base_url"])
    calendar_page.assert_on_create_page()


@when("the company user completes the calendar creation steps")
def company_user_completes_calendar_flow(page, calendar_payload, calendar_create_response):
    calendar_page = CalendarPage(page)

    calendar_page.select_direct_assign()
    calendar_page.fill_basic_details(
        calendar_name=calendar_payload["internal_calendar_name"],
        description=calendar_payload["internal_description"],
    )
    calendar_page.click_next()
    calendar_page.move_to_final_step()
    # Explicitly keep external name different from internal name.
    calendar_page.fill_external_calendar_details_if_visible(
        calendar_name=calendar_payload["external_calendar_name"],
        description=calendar_payload["external_description"],
    )

    status_code, response_body = calendar_page.submit_create_calendar_and_capture_api()
    calendar_create_response["status_code"] = status_code
    calendar_create_response["response_body"] = response_body
    calendar_create_response["calendar_name"] = calendar_payload["internal_calendar_name"]
    calendar_create_response["external_calendar_name"] = calendar_payload["external_calendar_name"]


@when("the company user completes the dispatcher calendar creation steps")
def company_user_completes_dispatcher_calendar_flow(page, calendar_payload, calendar_create_response):
    calendar_page = CalendarPage(page)

    calendar_page.select_dispatcher()
    calendar_page.fill_basic_details(
        calendar_name=calendar_payload["internal_calendar_name"],
        description=calendar_payload["internal_description"],
    )
    # Move from Basic Info (step 1) to Add Users (step 2).
    calendar_page.click_next()
    # On Add Users step, select Dispatcher role and continue.
    calendar_page.select_dispatcher_checkbox_and_continue()
    calendar_page.move_to_final_step()
    calendar_page.fill_external_calendar_details_if_visible(
        calendar_name=calendar_payload["external_calendar_name"],
        description=calendar_payload["external_description"],
    )

    status_code, response_body = calendar_page.submit_create_calendar_and_capture_api()
    calendar_create_response["status_code"] = status_code
    calendar_create_response["response_body"] = response_body
    calendar_create_response["calendar_name"] = calendar_payload["internal_calendar_name"]
    calendar_create_response["external_calendar_name"] = calendar_payload["external_calendar_name"]


@when("the company user completes direct assign flow with availability selections")
def company_user_completes_direct_assign_flow_with_availability(page, calendar_payload, calendar_create_response):
    calendar_page = CalendarPage(page)

    calendar_page.select_direct_assign()
    calendar_page.fill_basic_details(
        calendar_name=calendar_payload["internal_calendar_name"],
        description=calendar_payload["internal_description"],
    )
    calendar_page.click_next()
    calendar_page.select_first_two_participants()
    calendar_page.click_next()
    calendar_page.configure_availability_settings()
    calendar_page.click_next()
    calendar_page.move_to_final_step()
    calendar_page.fill_external_calendar_details_if_visible(
        calendar_name=calendar_payload["external_calendar_name"],
        description=calendar_payload["external_description"],
    )

    status_code, response_body = calendar_page.submit_create_calendar_and_capture_api()
    calendar_create_response["status_code"] = status_code
    calendar_create_response["response_body"] = response_body
    calendar_create_response["calendar_name"] = calendar_payload["internal_calendar_name"]
    calendar_create_response["external_calendar_name"] = calendar_payload["external_calendar_name"]


@when("the company user completes dispatcher flow with availability selections")
def company_user_completes_dispatcher_flow_with_availability(page, calendar_payload, calendar_create_response):
    calendar_page = CalendarPage(page)

    calendar_page.select_dispatcher()
    calendar_page.fill_basic_details(
        calendar_name=calendar_payload["internal_calendar_name"],
        description=calendar_payload["internal_description"],
    )
    calendar_page.click_next()
    calendar_page.select_dispatcher_checkbox_and_continue()
    calendar_page.click_next()
    calendar_page.configure_availability_settings()
    calendar_page.click_next()
    calendar_page.move_to_final_step()
    calendar_page.fill_external_calendar_details_if_visible(
        calendar_name=calendar_payload["external_calendar_name"],
        description=calendar_payload["external_description"],
    )

    status_code, response_body = calendar_page.submit_create_calendar_and_capture_api()
    calendar_create_response["status_code"] = status_code
    calendar_create_response["response_body"] = response_body
    calendar_create_response["calendar_name"] = calendar_payload["internal_calendar_name"]
    calendar_create_response["external_calendar_name"] = calendar_payload["external_calendar_name"]


@then("Calendar should be created")
def verify_calendar_create_success(calendar_create_response):
    status_code = calendar_create_response["status_code"]
    response_body = calendar_create_response["response_body"]
    calendar_name = calendar_create_response["calendar_name"]
    external_calendar_name = calendar_create_response["external_calendar_name"]

    with allure.step(
        f"Verify calendar create API status for internal={calendar_name}, external={external_calendar_name}"
    ):
        allure.attach(str(status_code), "calendar_create_status_code", allure.attachment_type.TEXT)
        allure.attach(response_body, "calendar_create_response", allure.attachment_type.JSON)
        assert status_code in {200, 201}, (
            f"Calendar create API failed with status {status_code}. "
            "See attached 'calendar_create_response' in Allure."
        )
