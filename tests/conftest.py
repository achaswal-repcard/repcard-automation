import sys
import os
import pytest
import allure
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.env_config import get_config
from playwright.sync_api import sync_playwright

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa")

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def config(env):
    return get_config(env)

@pytest.fixture(scope="session")
def browser():
    headless = os.getenv("HEADLESS", "false").lower() in {"1", "true", "yes"}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Attach a screenshot to Allure when a test fails (setup/call/teardown).
    """
    outcome = yield
    report = outcome.get_result()

    if report.failed and report.when in {"setup", "call", "teardown"}:
        page = item.funcargs.get("page")
        if page:
            screenshot = page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name=f"failure_{report.when}_{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )
            try:
                allure.attach(
                    page.url,
                    name="page_url",
                    attachment_type=allure.attachment_type.TEXT,
                )
            except Exception:
                # If page is already closed/unavailable during teardown
                pass


def pytest_bdd_before_scenario(request, feature, scenario):
    """
    Map BDD tags (e.g. @negative, @positive, @smoke) into Allure tags.
    """
    tags = set()
    if hasattr(feature, "tags") and feature.tags:
        tags.update(feature.tags)
    if hasattr(scenario, "tags") and scenario.tags:
        tags.update(scenario.tags)

    for tag in tags:
        allure.dynamic.tag(tag)
