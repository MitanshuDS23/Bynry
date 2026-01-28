import os
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = os.getenv("BASE_URL", "https://staging.workflowpro.com")
BROWSER = os.getenv("BROWSER", "chromium")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:

        browser_type = {
            "chromium": p.chromium,
            "firefox": p.firefox,
            "webkit": p.webkit,
        }.get(BROWSER, p.chromium)

        browser = browser_type.launch(headless=HEADLESS)
        yield browser
        browser.close()


@pytest.fixture()
def context(browser, request):


    context = browser.new_context(
        viewport={"width": 1280, "height": 800}
    )

    page = context.new_page()

    yield page


    if request.node.rep_call.failed:
        os.makedirs("artifacts/screenshots", exist_ok=True)
        page.screenshot(
            path=f"artifacts/screenshots/{request.node.name}.png",
            full_page=True
        )

    context.close()


@pytest.fixture(autouse=True)
def record_test_result(request):
 
    yield
    request.node.rep_call = getattr(request.node, "rep_call", None)


def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture test outcome.
    """
    if call.when == "call":
        item.rep_call = call


@pytest.fixture()
def page(context):
    """
    Returns a ready-to-use Playwright page object.
    """
    return context
