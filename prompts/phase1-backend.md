# Phase 1 — Backend Scaffold

You are working on a project called Meeter. Start every iteration by reading
these files in order:

1. /root/meeter/CLAUDE.md — conventions and stack decisions
2. /root/meeter/PRD.md — product requirements
3. /root/meeter/CHECKLIST.md — your progress tracker

Then check what files currently exist under /root/meeter/backend/.

Your job is to complete every unchecked item under "Phase 1 — Backend Scaffold"
in CHECKLIST.md. Work through them one at a time. After completing each item,
mark it [x] in CHECKLIST.md before moving to the next.

---

## What to build

Create the following files under /root/meeter/backend/:

### requirements.txt
Include these packages:
fastapi, uvicorn, sqlmodel, anthropic, faster-whisper, python-dotenv,
pytest, pytest-asyncio, httpx

### .env.example
Empty values for: ANTHROPIC_API_KEY, SMTP_HOST, SMTP_PORT, SMTP_USER,
SMTP_PASSWORD, SMTP_FROM

### database.py
- Create a SQLite engine pointed at meeter.db
- Expose a `get_session` dependency function that yields a Session
- Call `SQLModel.metadata.create_all(engine)` on startup via a lifespan function

### models.py
Define three SQLModel table models:
- `StaffMember`: id (int, pk), name (str), email (str), slack_handle (Optional[str])
- `Meeting`: id (int, pk), title (str), created_at (datetime, default now),
  status (str, default "recording"), transcript (str, default "")
- `Task`: id (int, pk), meeting_id (int, FK to meeting.id), description (str),
  assignee_id (Optional[int]), due_date (Optional[str]), sent_at (Optional[datetime])

### routes/__init__.py
Empty file.

### routes/meetings.py
Empty APIRouter — no endpoints yet. Just:
```python
from fastapi import APIRouter
router = APIRouter()
```

### routes/staff.py
Empty APIRouter — no endpoints yet. Same pattern as meetings.py.

### services/__init__.py
Empty file.

### services/transcription.py
Empty module. Add a comment: # Whisper transcription service — implemented in Phase 5

### services/extraction.py
Empty module. Add a comment: # Claude task extraction service — implemented in Phase 6

### services/email.py
Empty module. Add a comment: # Email delivery service — implemented in Phase 8

### main.py
- Create a FastAPI app using a lifespan context manager
- In the lifespan, call the database init (create_all)
- Include the meetings and staff routers
- Export `get_session` (re-export from database.py so conftest.py can import it)
- Add `GET /health` that returns `{"status": "ok"}`

---

## Verification

After you believe all files are in place, run:

```
cd /root/meeter/backend && pytest tests/test_health.py -v
```

If the test fails, read the error carefully, fix the root cause, and run again.
Do not move on until the test passes.

---

## Completion

When `pytest tests/test_health.py` passes with no errors and all Phase 1
backend items in CHECKLIST.md are marked [x], output exactly:

<promise>PHASE1_BACKEND_COMPLETE</promise>

Do not output the promise until the test actually passes.
