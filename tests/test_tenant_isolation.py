import requests

BASE_URL = "https://staging.workflowpro.com"

def test_cross_tenant_access_denied():
    """
    Verify that a token from Tenant A cannot access
    resources when Tenant B is supplied in headers.
    """

    token = "COMPANY1_TOKEN"

    # Valid tenant access
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

    # Cross-tenant attempt with same token
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

    # Optional
    body = r2.json()
    assert "tenant" in body.get("message", "").lower() or \
           "unauthorized" in body.get("message", "").lower()
