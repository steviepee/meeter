# Meeter — Task List

Tasks are processed in order. Do not skip ahead.
Each task has: Status (PENDING / DONE / BLOCKED), Description, and Verify.

---

## Phase 1 — Backend Scaffold

### Task: Create backend requirements.txt
Status: DONE
Description: Create /root/meeter/backend/requirements.txt with these packages:
  fastapi, uvicorn, sqlmodel, anthropic, faster-whisper, python-dotenv,
  pytest, pytest-asyncio, httpx
Verify: cd /root/meeter/backend && pip install -r requirements.txt --dry-run

---

### Task: Create backend .env.example
Status: DONE
Description: Create /root/meeter/backend/.env.example with empty values for:
  ANTHROPIC_API_KEY, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM
Verify: File exists at /root/meeter/backend/.env.example

---

### Task: Create database.py
Status: DONE
Description: Create /root/meeter/backend/database.py with:
  - SQLite engine pointed at meeter.db
  - get_session dependency function that yields a Session
  - create_db_and_tables() function that calls SQLModel.metadata.create_all(engine)
Verify: cd /root/meeter/backend && python -c "from database import get_session, create_db_and_tables; print('OK')"

---

### Task: Create models.py
Status: DONE
Description: Create /root/meeter/backend/models.py defining three SQLModel table models:
  - StaffMember: id (int pk), name (str), email (str), slack_handle (Optional[str])
  - Meeting: id (int pk), title (str), created_at (datetime default now),
    status (str default "recording"), transcript (str default "")
  - Task: id (int pk), meeting_id (int FK to meeting.id), description (str),
    assignee_id (Optional[int]), due_date (Optional[str]), sent_at (Optional[datetime])
Verify: cd /root/meeter/backend && python -c "from models import StaffMember, Meeting, Task; print('OK')"

---

### Task: Create routes and services stubs
Status: DONE
Description: Create the following empty stub files:
  - /root/meeter/backend/routes/__init__.py (empty)
  - /root/meeter/backend/routes/meetings.py (APIRouter stub, no endpoints)
  - /root/meeter/backend/routes/staff.py (APIRouter stub, no endpoints)
  - /root/meeter/backend/services/__init__.py (empty)
  - /root/meeter/backend/services/transcription.py (comment: # Whisper — Phase 5)
  - /root/meeter/backend/services/extraction.py (comment: # Claude extraction — Phase 6)
  - /root/meeter/backend/services/email.py (comment: # Email delivery — Phase 8)
Verify: cd /root/meeter/backend && python -c "from routes.meetings import router; from routes.staff import router; print('OK')"

---

### Task: Create main.py and pass health check test
Status: DONE
Description: Create /root/meeter/backend/main.py with:
  - FastAPI app using a lifespan context manager that calls create_db_and_tables()
  - meetings and staff routers included
  - get_session re-exported from database.py (conftest.py imports it from main)
  - GET /health endpoint returning {"status": "ok"}
Verify: cd /root/meeter/backend && pytest tests/test_health.py -v

---

## Phase 1 — Frontend Scaffold

### Task: Scaffold Vite React TypeScript project
Status: DONE
Description: If /root/meeter/frontend/package.json does not exist, run:
  cd /root/meeter && npm create vite@latest frontend -- --template react-ts
  Then run: cd /root/meeter/frontend && npm install
Verify: File exists at /root/meeter/frontend/package.json

---

### Task: Install frontend dependencies
Status: DONE
Description: From /root/meeter/frontend run:
  npm install react-router-dom @tanstack/react-query
  npm install tailwindcss @tailwindcss/vite
Verify: cd /root/meeter/frontend && node -e "require('./node_modules/react-router-dom/package.json'); console.log('OK')"

---

### Task: Configure Tailwind CSS
Status: DONE
Description: In /root/meeter/frontend/vite.config.ts add the @tailwindcss/vite plugin.
  Replace contents of /root/meeter/frontend/src/index.css with: @import "tailwindcss";
Verify: cd /root/meeter/frontend && npm run build 2>&1 | grep -v "tailwind" | head -5

---

### Task: Create page shells and API placeholder
Status: DONE
Description: Create:
  - /root/meeter/frontend/src/api/index.ts (placeholder comment)
  - /root/meeter/frontend/src/pages/MeetingPage.tsx (returns <div>Meeting</div>)
  - /root/meeter/frontend/src/pages/TaskListPage.tsx (returns <div>Tasks</div>)
  - /root/meeter/frontend/src/pages/SettingsPage.tsx (returns <div>Settings</div>)
Verify: All four files exist

---

### Task: Wire up routing and QueryClientProvider
Status: DONE
Description: Replace /root/meeter/frontend/src/App.tsx with React Router routes:
  / → MeetingPage, /tasks → TaskListPage, /settings → SettingsPage
  Wrap <App /> in QueryClientProvider in /root/meeter/frontend/src/main.tsx
  Create /root/meeter/frontend/.env.example with VITE_API_BASE_URL=http://localhost:8000
Verify: cd /root/meeter/frontend && npm run build

---

## Phase 2 — Data Models & Database

### Task: Verify DB tables create on startup
Status: DONE
Description: Confirm that running create_db_and_tables() actually creates all three
  tables in a test SQLite DB. Fix models.py or database.py if needed.
Verify: cd /root/meeter/backend && python -c "
from sqlmodel import create_engine, Session, SQLModel
engine = create_engine('sqlite:///test_verify.db')
from models import StaffMember, Meeting, Task
SQLModel.metadata.create_all(engine)
import sqlite3, os
conn = sqlite3.connect('test_verify.db')
tables = conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()
conn.close()
os.remove('test_verify.db')
assert len(tables) == 3, f'Expected 3 tables, got {tables}'
print('OK')
"

---

## Phase 3 — Staff Roster API + Settings UI

### Task: Implement staff API endpoints
Status: DONE
Description: In /root/meeter/backend/routes/staff.py implement:
  GET /staff — list all staff
  POST /staff — create staff member (body: name, email, slack_handle)
  PUT /staff/{id} — update staff member
  DELETE /staff/{id} — delete staff member
  Register router in main.py with prefix /staff
Verify: cd /root/meeter/backend && pytest tests/test_staff.py -v

---

### Task: Write staff API tests
Status: DONE
Description: Fill in /root/meeter/backend/tests/test_staff.py with tests covering:
  - POST /staff creates a staff member and returns it
  - GET /staff returns a list including the created member
  - PUT /staff/{id} updates fields correctly
  - DELETE /staff/{id} removes the member
Verify: cd /root/meeter/backend && pytest tests/test_staff.py -v

---

### Task: Build SettingsPage staff roster UI
Status: DONE
Description: Implement /root/meeter/frontend/src/pages/SettingsPage.tsx with:
  - List of staff members fetched via TanStack Query
  - Add staff form (name, email, slack_handle fields)
  - Delete button per staff member
  - API hooks in src/api/index.ts for staff CRUD
Verify: cd /root/meeter/frontend && npm run build

---

## Phase 4 — Meeting Sessions API

### Task: Implement meeting API endpoints
Status: DONE
Description: In /root/meeter/backend/routes/meetings.py implement:
  POST /meetings — create new meeting, returns id
  GET /meetings — list all meetings
  GET /meetings/{id} — get single meeting with tasks
  PATCH /meetings/{id} — update status
  POST /meetings/{id}/transcript — append transcript chunk
  Register router in main.py with prefix /meetings
Verify: cd /root/meeter/backend && pytest tests/test_meetings.py -v

---

### Task: Write meeting API tests
Status: DONE
Description: Fill in /root/meeter/backend/tests/test_meetings.py with tests covering:
  - POST /meetings creates a meeting and returns id
  - GET /meetings/{id} returns the meeting
  - PATCH /meetings/{id} updates status correctly
  - POST /meetings/{id}/transcript appends to transcript field
Verify: cd /root/meeter/backend && pytest tests/test_meetings.py -v

---

## Phase 5 — Live Transcription

### Task: Implement Whisper transcription service
Status: DONE
Description: Implement /root/meeter/backend/services/transcription.py:
  - Load faster-whisper WhisperModel (base, device=cpu) on module import
  - transcribe_chunk(audio_bytes: bytes) -> str function
  - POST /meetings/{id}/transcript/chunk endpoint that accepts audio blob,
    transcribes it, appends result to meeting transcript, returns new text
  - GET /meetings/{id}/transcript/stream SSE endpoint streaming transcript updates
Verify: cd /root/meeter/backend && python -c "from services.transcription import transcribe_chunk; print('OK')"

---

### Task: Build live transcript UI
Status: DONE
Description: Implement /root/meeter/frontend/src/pages/MeetingPage.tsx:
  - Start/Stop recording buttons using browser MediaRecorder API
  - On start: POST /meetings to create session, begin recording mic audio
  - Send audio blobs to POST /meetings/{id}/transcript/chunk
  - Connect to SSE stream and display rolling transcript text
  - On stop: PATCH /meetings/{id} status to "reviewing", trigger extraction
Verify: cd /root/meeter/frontend && npm run build

---

## Phase 6 — Task Extraction (Claude)

### Task: Implement Claude task extraction service
Status: DONE
Description: Implement /root/meeter/backend/services/extraction.py:
  - EXTRACTION_PROMPT constant with the full prompt (include staff roster + transcript)
  - extract_tasks(transcript: str, staff: list) -> list[dict] function using
    anthropic client with claude-sonnet-4-6 and tool use or JSON mode
  - Each returned task: {description, assignee_id, due_date, confidence}
  - POST /meetings/{id}/extract endpoint that calls extraction and saves tasks to DB
Verify: cd /root/meeter/backend && pytest tests/test_extraction.py -v

---

### Task: Write extraction tests
Status: DONE
Description: Fill in /root/meeter/backend/tests/test_extraction.py:
  - Mock the Anthropic client
  - Test that extract_tasks returns correct structure from a sample transcript
  - Test that POST /meetings/{id}/extract saves tasks to DB
Verify: cd /root/meeter/backend && pytest tests/test_extraction.py -v

---

## Phase 7 — Task Review UI

### Task: Build task review UI
Status: DONE
Description: Extend MeetingPage.tsx to show review mode after recording stops:
  - Display extracted tasks list (description, assignee dropdown, due date)
  - Assignee dropdown populated from staff roster
  - Inline edit task description
  - Delete task button
  - Add task button
  - Low-confidence tasks visually flagged
  - "Confirm & Send" button calls POST /meetings/{id}/send
Verify: cd /root/meeter/frontend && npm run build

---

## Phase 8 — Email Delivery

### Task: Implement email delivery service
Status: DONE
Description: Implement /root/meeter/backend/services/email.py:
  - send_tasks_email(staff_member, tasks) function using smtplib and env vars
  - Batch tasks by assignee — one email per person
  - Plain text email body listing tasks with descriptions and due dates
  - POST /meetings/{id}/send endpoint: saves tasks, sends emails, sets sent_at
Verify: cd /root/meeter/backend && pytest tests/test_email.py -v

---

### Task: Write email delivery tests
Status: DONE
Description: Fill in /root/meeter/backend/tests/test_email.py:
  - Mock smtplib.SMTP
  - Test that send_tasks_email sends one email per unique assignee
  - Test that sent_at is set on tasks after POST /meetings/{id}/send
Verify: cd /root/meeter/backend && pytest tests/test_email.py -v

---

## Phase 9 — Task List View

### Task: Build task list page
Status: DONE
Description: Implement /root/meeter/frontend/src/pages/TaskListPage.tsx:
  - List all meetings (title, date, status, task count) via GET /meetings
  - Clicking a meeting expands to show confirmed tasks grouped by assignee
  - Empty state for no meetings
Verify: cd /root/meeter/frontend && npm run build

---

## Phase 10 — Integration & Polish

### Task: End-to-end verification and polish
Status: DONE
Description: Verify the full flow works:
  - CORS configured in main.py for localhost:5173
  - No hardcoded localhost URLs in frontend (use import.meta.env.VITE_API_BASE_URL)
  - All loading states present on async operations
  - Error messages shown on API failures
  - README.md updated with setup and run instructions
  - .env.example files are complete and accurate
Verify: cd /root/meeter/backend && pytest -v && cd /root/meeter/frontend && npm run build
