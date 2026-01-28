import pytest
from playwright.sync_api import expect

BASE_URL = "https://staging.workflowpro.com"

def test_login_admin(page):
    """
    Verify that an Admin user can log in successfully
    and is redirected to the dashboard.
    """

    page.goto(f"{BASE_URL}/login", wait_until="networkidle")

    # Fill credentials
    page.locator("[data-test-id=email]").fill("admin@company1.com")
    page.locator("[data-test-id=password]").fill("Password123")

    # Click login and wait for navigation
    with page.expect_navigation(url="**/dashboard"):
        page.locator("[data-test-id=login-btn]").click()

    # Dashboard visible
    dashboard_header = page.locator("[data-test-id=dashboard-title]")
    expect(dashboard_header).to_be_visible(timeout=10000)


    user_badge = page.locator("[data-test-id=user-role]")
    expect(user_badge).to_have_text("Admin")

    # Optional
    cookies = page.context.cookies()
    assert any("session" in c["name"].lower() for c in cookies)
