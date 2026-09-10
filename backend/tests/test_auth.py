def test_register(client):
    r = client.post("/auth/register", json={"email": "new@test.com", "password": "pass1234"})
    assert r.status_code == 200

def test_duplicate_register(client):
    client.post("/auth/register", json={"email": "dup@test.com", "password": "pass1234"})
    r = client.post("/auth/register", json={"email": "dup@test.com", "password": "pass1234"})
    assert r.status_code == 400

def test_login_returns_token(client):
    client.post("/auth/register", json={"email": "login@test.com", "password": "pass1234"})
    r = client.post("/auth/login", data={"username": "login@test.com", "password": "pass1234"})
    assert r.status_code == 200
    assert "access_token" in r.json()

def test_wrong_password(client):
    client.post("/auth/register", json={"email": "wp@test.com", "password": "correct"})
    r = client.post("/auth/login", data={"username": "wp@test.com", "password": "wrong"})
    assert r.status_code == 401