from unittest.mock import MagicMock, patch


SAMPLE_TASKS = [
    {"description": "Write report", "assignee_id": None, "due_date": "2026-03-20", "confidence": 0.9},
    {"description": "Send email to Alice", "assignee_id": 1, "due_date": None, "confidence": 0.8},
]


def _make_mock_message(tasks):
    block = MagicMock()
    block.type = "tool_use"
    block.name = "save_tasks"
    block.input = {"tasks": tasks}
    msg = MagicMock()
    msg.content = [block]
    return msg


def test_extract_tasks_returns_structure():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _make_mock_message(SAMPLE_TASKS)

    with patch("services.extraction._get_client", return_value=mock_client):
        from services.extraction import extract_tasks
        results = extract_tasks("Alice will write a report by Friday.", [{"id": 1, "name": "Alice"}])

    assert len(results) == 2
    assert results[0]["description"] == "Write report"
    assert results[1]["assignee_id"] == 1


def test_extract_endpoint_saves_tasks(client):
    # Create a meeting
    create = client.post("/meetings", json={"title": "Test Meeting"})
    meeting_id = create.json()["id"]
    client.post(f"/meetings/{meeting_id}/transcript", json={"text": "Alice will write a report."})

    mock_client = MagicMock()
    mock_client.messages.create.return_value = _make_mock_message(SAMPLE_TASKS)

    with patch("services.extraction._get_client", return_value=mock_client):
        response = client.post(f"/meetings/{meeting_id}/extract")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["meeting_id"] == meeting_id
