def test_create_meeting(client):
    response = client.post("/meetings", json={"title": "Sprint Planning"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Sprint Planning"
    assert data["id"] is not None
    assert data["status"] == "recording"


def test_get_meeting(client):
    create = client.post("/meetings", json={"title": "Standup"})
    meeting_id = create.json()["id"]
    response = client.get(f"/meetings/{meeting_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Standup"


def test_update_meeting_status(client):
    create = client.post("/meetings", json={"title": "Retro"})
    meeting_id = create.json()["id"]
    response = client.patch(f"/meetings/{meeting_id}", json={"status": "reviewing"})
    assert response.status_code == 200
    assert response.json()["status"] == "reviewing"


def test_append_transcript(client):
    create = client.post("/meetings", json={"title": "All Hands"})
    meeting_id = create.json()["id"]
    client.post(f"/meetings/{meeting_id}/transcript", json={"text": "Hello world"})
    response = client.post(f"/meetings/{meeting_id}/transcript", json={"text": "more text"})
    assert response.status_code == 200
    assert "Hello world" in response.json()["transcript"]
    assert "more text" in response.json()["transcript"]
