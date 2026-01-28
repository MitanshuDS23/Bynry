
def test_login_admin(page):
    page.goto("https://staging.workflowpro.com/login")
    page.fill("[data-test-id=email]", "admin@company1.com")
    page.fill("[data-test-id=password]", "Password123")
    page.click("[data-test-id=login-btn]")
    page.wait_for_url("**/dashboard")
    assert page.locator("text=Dashboard").is_visible()
