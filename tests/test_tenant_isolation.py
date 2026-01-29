import requests

BASE_URL = "https://staging.workflowpro.com"

def test_cross_tenant_access_denied():
    token = "COMPANY1_TOKEN"

    headers_company1 = {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": "company1"
    }

    r1 = requests.get(
        f"{BASE_URL}/api/projects",
        headers=headers_company1,
        timeout=10
    )
    assert r1.status_code == 200

    headers_company2 = {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": "company2"
    }

    r2 = requests.get(
        f"{BASE_URL}/api/projects",
        headers=headers_company2,
        timeout=10
    )
    assert r2.status_code in (401, 403)

    if r2.headers.get("content-type", "").startswith("application/json"):
        body = r2.json()
        msg = (body.get("message") or body.get("error") or "").lower()
        assert "tenant" in msg or "unauthorized" in msg
