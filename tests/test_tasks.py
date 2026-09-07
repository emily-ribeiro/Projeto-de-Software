def test_create_task(client, auth_headers):
    response = client.post(
        "/tasks/",
        json={"title": "Estudar FastAPI", "priority": "high"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Estudar FastAPI"
    assert data["status"] == "pending"
    assert data["priority"] == "high"


def test_list_tasks_only_own(client, auth_headers):
    client.post("/tasks/", json={"title": "Tarefa 1"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Tarefa 2"}, headers=auth_headers)

    client.post("/auth/register", json={"username": "other", "password": "pass123456"})
    other_login = client.post(
        "/auth/login",
        data={"username": "other", "password": "pass123456"},
    )
    other_headers = {"Authorization": f"Bearer {other_login.json()['access_token']}"}
    client.post("/tasks/", json={"title": "Tarefa de outro"}, headers=other_headers)

    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert all(task["title"] != "Tarefa de outro" for task in response.json())


def test_get_task_not_found(client, auth_headers):
    response = client.get("/tasks/999", headers=auth_headers)
    assert response.status_code == 404


def test_update_task(client, auth_headers):
    create_resp = client.post("/tasks/", json={"title": "Original"}, headers=auth_headers)
    task_id = create_resp.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"status": "done", "title": "Atualizado"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"
    assert data["title"] == "Atualizado"


def test_delete_task(client, auth_headers):
    create_resp = client.post("/tasks/", json={"title": "Para deletar"}, headers=auth_headers)
    task_id = create_resp.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

    get_resp = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_filter_tasks_by_status(client, auth_headers):
    client.post("/tasks/", json={"title": "A", "status": "done"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "B", "status": "pending"}, headers=auth_headers)

    response = client.get("/tasks/?status=done", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "A"


def test_cannot_access_other_users_task(client, db_session):
    # user 1 creates a task
    client.post("/auth/register", json={"username": "user1", "password": "pass123456"})
    login1 = client.post("/auth/login", data={"username": "user1", "password": "pass123456"})
    headers1 = {"Authorization": f"Bearer {login1.json()['access_token']}"}
    create_resp = client.post("/tasks/", json={"title": "Privada"}, headers=headers1)
    task_id = create_resp.json()["id"]

    # user 2 tries to access it
    client.post("/auth/register", json={"username": "user2", "password": "pass123456"})
    login2 = client.post("/auth/login", data={"username": "user2", "password": "pass123456"})
    headers2 = {"Authorization": f"Bearer {login2.json()['access_token']}"}

    response = client.get(f"/tasks/{task_id}", headers=headers2)
    assert response.status_code == 403
