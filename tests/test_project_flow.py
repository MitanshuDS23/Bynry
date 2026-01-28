import requests
import uuid
import pytest
from playwright.sync_api import expect

BASE_URL = "https://staging.workflowpro.com"

def test_project_creation_and_ui_visibility(page):


    token = "COMPANY1_TOKEN"
    tenant_id = "company1"

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": tenant_id,
        "Content-Type": "application/json"
    }

    project_name = f"auto-project-{uuid.uuid4().hex[:8]}"

    payload = {
        "name": project_name,
        "description": "Created by automation test"
    }

    # ---- API: Create project ----
    response = requests.post(
        f"{BASE_URL}/api/projects",
        json=payload,
        headers=headers,
        timeout=10
    )

    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    project_id = body["id"]

    try:
 
        page.goto(f"{BASE_URL}/dashboard", wait_until="networkidle")

        search_box = page.locator("[data-test-id=search-project]")
        search_box.fill(project_name)

        project_row = page.locator(f"text={project_name}")
        expect(project_row).to_be_visible(timeout=15000)

    finally:
       
        requests.delete(
            f"{BASE_URL}/api/projects/{project_id}",
            headers=headers,
            timeout=10
        )
