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
    browser_channel = os.getenv("BROWSER_CHANNEL")
    with sync_playwright() as p:
        launch_kwargs = {"headless": headless}
        if browser_channel:
            launch_kwargs["channel"] = browser_channel
        browser = p.chromium.launch(**launch_kwargs)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture
def assert_page_healthy():
    """
    Fail fast when backend/debug error pages are returned instead of app UI.
    """
    error_markers = (
        "cannot redeclare",
        "fatalerror",
        "stack trace",
        "symfony\\component\\errorhandler",
        "whoops",
    )

    def _assert(page, response=None):
        status = response.status if response else None
        title = ""
        content = ""
        try:
            title = page.title()
            content = page.content()
        except Exception:
            pass

        title_lower = title.lower() if title else ""
        content_lower = content.lower() if content else ""
        matched = [m for m in error_markers if m in title_lower or m in content_lower]
        reasons = []

        if status is not None and status >= 500:
            reasons.append(f"HTTP {status}")
        if matched:
            reasons.append(f"error markers: {', '.join(matched)}")

        if reasons:
            allure.attach(page.url, name="env_page_url", attachment_type=allure.attachment_type.TEXT)
            allure.attach(title or "<no title>", name="env_page_title", attachment_type=allure.attachment_type.TEXT)
            snippet = content[:4000] if content else "<no content>"
            allure.attach(snippet, name="env_page_snippet", attachment_type=allure.attachment_type.HTML)
            raise AssertionError(f"QA environment unhealthy on login page ({'; '.join(reasons)})")

    return _assert


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
