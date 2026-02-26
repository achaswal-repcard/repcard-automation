import allure
import time

import pytest
from pytest_bdd import given, parsers, scenario, then, when

from pages.web.login_page import LoginPage
from pages.web.sidebar_page import SidebarPage


@scenario(
    "sidebar_navigation.feature",
    "Sidebar links redirect correctly in left-panel order",
)
def test_sidebar_links_redirect_in_order():
    pass


@pytest.fixture
def sidebar_context():
    return {}


@given("the user is logged in to admin home with valid credentials")
def user_logged_in_to_admin_home(page, config, assert_page_healthy):
    last_error = None
    for attempt in range(1, 4):
        try:
            response = page.goto(f"{config['base_url']}/admin/login", wait_until="domcontentloaded")
            assert_page_healthy(page, response)

            page.locator("input[name='email']").wait_for(state="visible", timeout=10000)

            login_page = LoginPage(page)
            login_page.enter_username("admin@repcard.com")
            login_page.enter_password("Repcard1$")
            login_page.click_login()
            page.wait_for_url("**/admin/home", timeout=10000)
            assert "/admin/home" in page.url
            return
        except Exception as exc:
            last_error = exc
            if attempt < 3:
                time.sleep(2)
                continue
            raise AssertionError(
                f"Unable to login after 3 attempts due to unstable environment: {last_error}"
            )


@when(parsers.parse('the user clicks "{menu_path}" from left sidebar'))
def click_left_sidebar_path(page, menu_path, config, sidebar_context):
    allure.dynamic.title(f"Sidebar links redirect correctly in left-panel order - {menu_path}")
    sidebar_context["menu_path"] = menu_path
    sidebar_page = SidebarPage(page)
    sidebar_page.go_to_home_page(config["base_url"])
    sidebar_page.click_sidebar_path(menu_path)


@then(parsers.parse('the user should land on URL containing "{expected_url_part}"'))
def verify_left_sidebar_redirect(page, expected_url_part, sidebar_context):
    menu_path = sidebar_context.get("menu_path", "selected link")
    with allure.step(f"Redirection to {menu_path} successful"):
        SidebarPage(page).verify_redirect(expected_url_part)
