def test_create_staff(client):
    response = client.post("/staff", json={"name": "Alice", "email": "alice@example.com", "slack_handle": "@alice"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["id"] is not None


def test_list_staff(client):
    client.post("/staff", json={"name": "Bob", "email": "bob@example.com", "slack_handle": None})
    response = client.get("/staff")
    assert response.status_code == 200
    members = response.json()
    assert any(m["name"] == "Bob" for m in members)


def test_update_staff(client):
    create = client.post("/staff", json={"name": "Carol", "email": "carol@example.com", "slack_handle": None})
    member_id = create.json()["id"]
    response = client.put(f"/staff/{member_id}", json={"name": "Carol Updated", "email": "carol2@example.com", "slack_handle": "@carol"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Carol Updated"
    assert data["email"] == "carol2@example.com"


def test_delete_staff(client):
    create = client.post("/staff", json={"name": "Dave", "email": "dave@example.com", "slack_handle": None})
    member_id = create.json()["id"]
    response = client.delete(f"/staff/{member_id}")
    assert response.status_code == 204
    get = client.get("/staff")
    assert all(m["id"] != member_id for m in get.json())
