def test_register_user(client):
    response = client.post("/auth/register", json={"username": "alice", "password": "secret123"})
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert "id" in data


def test_register_duplicate_username(client):
    client.post("/auth/register", json={"username": "bob", "password": "secret123"})
    response = client.post("/auth/register", json={"username": "bob", "password": "other123"})
    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={"username": "carol", "password": "secret123"})
    response = client.post("/auth/login", data={"username": "carol", "password": "secret123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "dave", "password": "secret123"})
    response = client.post("/auth/login", data={"username": "dave", "password": "wrongpass"})
    assert response.status_code == 401


def test_access_protected_route_without_token(client):
    response = client.get("/tasks/")
    assert response.status_code == 401
