from unittest.mock import MagicMock, patch


STAFF = {"id": 1, "name": "Alice", "email": "alice@example.com"}
TASKS = [
    {"description": "Write report", "assignee_id": 1, "due_date": "2026-03-20"},
    {"description": "Send email", "assignee_id": 1, "due_date": None},
]


def test_send_tasks_email_sends_one_email_per_assignee():
    mock_smtp_instance = MagicMock()
    mock_smtp_class = MagicMock(return_value=mock_smtp_instance)
    mock_smtp_instance.__enter__ = MagicMock(return_value=mock_smtp_instance)
    mock_smtp_instance.__exit__ = MagicMock(return_value=False)

    with patch("smtplib.SMTP", mock_smtp_class):
        from services.email import send_tasks_email
        send_tasks_email(STAFF, TASKS)

    mock_smtp_instance.sendmail.assert_called_once()
    call_args = mock_smtp_instance.sendmail.call_args
    assert call_args[0][1] == ["alice@example.com"]


def test_send_endpoint_sets_sent_at(client):
    # Create staff and meeting
    staff_res = client.post("/staff", json={"name": "Alice", "email": "alice@example.com", "slack_handle": None})
    staff_id = staff_res.json()["id"]
    meeting_res = client.post("/meetings", json={"title": "Test"})
    meeting_id = meeting_res.json()["id"]

    tasks_payload = [
        {"description": "Do thing", "assignee_id": staff_id, "due_date": None},
    ]

    mock_smtp_instance = MagicMock()
    mock_smtp_class = MagicMock(return_value=mock_smtp_instance)
    mock_smtp_instance.__enter__ = MagicMock(return_value=mock_smtp_instance)
    mock_smtp_instance.__exit__ = MagicMock(return_value=False)

    with patch("smtplib.SMTP", mock_smtp_class):
        res = client.post(f"/meetings/{meeting_id}/send", json={"tasks": tasks_payload})

    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    mock_smtp_instance.sendmail.assert_called_once()
