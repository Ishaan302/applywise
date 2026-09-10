def test_create_application(client, auth_headers):
    r = client.post("/applications", json={
        "company": "Google", "role": "SDE Intern"
    }, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["company"] == "Google"

def test_list_applications(client, auth_headers):
    r = client.get("/applications", headers=auth_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_update_status(client, auth_headers):
    create = client.post("/applications", json={
        "company": "Meta", "role": "ML Intern"
    }, headers=auth_headers)
    app_id = create.json()["id"]
    r = client.patch(f"/applications/{app_id}", json={"status": "Interview"}, headers=auth_headers)
    assert r.json()["status"] == "Interview"

def test_unauthorized_returns_401(client):
    r = client.get("/applications")
    assert r.status_code == 401

def test_user_isolation(client):
    client.post("/auth/register", json={"email": "a@iso.com", "password": "pass1234"})
    r = client.post("/auth/login", data={"username": "a@iso.com", "password": "pass1234"})
    headers_a = {"Authorization": f"Bearer {r.json()['access_token']}"}
    app_res = client.post("/applications", json={"company": "A Corp", "role": "Dev"}, headers=headers_a)
    app_id = app_res.json()["id"]

    client.post("/auth/register", json={"email": "b@iso.com", "password": "pass1234"})
    r = client.post("/auth/login", data={"username": "b@iso.com", "password": "pass1234"})
    headers_b = {"Authorization": f"Bearer {r.json()['access_token']}"}
    r = client.get(f"/applications/{app_id}", headers=headers_b)
    assert r.status_code == 404  # not 200 — this is what proves isolation actually works