
import requests

def test_cross_tenant_access_denied():
    token = "COMPANY1_TOKEN"
    headers = {"Authorization": f"Bearer {token}", "X-Tenant-ID": "company1"}
    r = requests.get("https://staging.workflowpro.com/api/projects", headers=headers)
    assert r.status_code == 200

    headers["X-Tenant-ID"] = "company2"
    r2 = requests.get("https://staging.workflowpro.com/api/projects", headers=headers)
    assert r2.status_code in (401,403)
