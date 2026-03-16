# Email delivery — Phase 8
import os
import smtplib
from email.mime.text import MIMEText


def send_tasks_email(staff_member: dict, tasks: list) -> None:
    lines = [f"Hi {staff_member['name']},\n\nYour action items from the meeting:\n"]
    for i, t in enumerate(tasks, 1):
        due = f" (due: {t['due_date']})" if t.get("due_date") else ""
        lines.append(f"{i}. {t['description']}{due}")
    lines.append("\nPlease complete these at your earliest convenience.")
    body = "\n".join(lines)

    msg = MIMEText(body)
    msg["Subject"] = "Your Meeting Action Items"
    msg["From"] = os.environ.get("SMTP_FROM", "noreply@meeter.local")
    msg["To"] = staff_member["email"]

    host = os.environ.get("SMTP_HOST", "localhost")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER", "")
    password = os.environ.get("SMTP_PASSWORD", "")

    with smtplib.SMTP(host, port) as server:
        if user:
            server.starttls()
            server.login(user, password)
        server.sendmail(msg["From"], [msg["To"]], msg.as_string())
