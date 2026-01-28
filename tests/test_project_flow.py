
import requests

def test_project_creation_and_ui_visibility(page):
    headers = {
        "Authorization": "Bearer COMPANY1_TOKEN",
        "X-Tenant-ID": "company1"
    }

    payload = {"name": "Automation Project", "description": "Created by test"}
    r = requests.post("https://staging.workflowpro.com/api/projects", json=payload, headers=headers)
    assert r.status_code == 201
    project_id = r.json()["id"]

    page.goto("https://staging.workflowpro.com/dashboard")
    page.fill("[data-test-id=search-project]", "Automation Project")
    assert page.locator("text=Automation Project").is_visible()

    requests.delete(f"https://staging.workflowpro.com/api/projects/{project_id}", headers=headers)
