# Meeter — Build Checklist

Track progress phase by phase. Each phase is a self-contained Ralph loop target.

---

## Phase 1 — Project Scaffold
> Goal: empty but runnable backend and frontend with correct structure

- [ ] Create `backend/` directory with `main.py`, `database.py`, `models.py`
- [ ] Create `backend/routes/` with `meetings.py` and `staff.py`
- [ ] Create `backend/services/` with `transcription.py`, `extraction.py`, `email.py`
- [ ] Create `backend/requirements.txt` with all dependencies
- [ ] Create `backend/.env.example` with all required env vars
- [ ] FastAPI app boots with `uvicorn main:app --reload` and returns 200 on `GET /health`
- [ ] Create `frontend/` via Vite + React + TypeScript template
- [ ] Install and configure TailwindCSS
- [ ] Install TanStack Query
- [ ] Create page shell files: `MeetingPage.tsx`, `TaskListPage.tsx`, `SettingsPage.tsx`
- [ ] Set up React Router with routes for `/`, `/tasks`, `/settings`
- [ ] Frontend dev server runs without errors

---

## Phase 2 — Data Models & Database
> Goal: SQLite DB with all tables created on startup

- [ ] Define `StaffMember` SQLModel (id, name, email, slack_handle)
- [ ] Define `Meeting` SQLModel (id, title, created_at, status, transcript)
- [ ] Define `Task` SQLModel (id, meeting_id, description, assignee_id, due_date, sent_at)
- [ ] `database.py` creates all tables on app startup
- [ ] Alembic or manual migration approach decided and documented

---

## Phase 3 — Staff Roster API + Settings UI
> Goal: organizer can add/edit/delete staff members

**Backend**
- [ ] `GET /staff` — list all staff
- [ ] `POST /staff` — create staff member
- [ ] `PUT /staff/{id}` — update staff member
- [ ] `DELETE /staff/{id}` — delete staff member

**Frontend**
- [ ] `SettingsPage` displays staff list
- [ ] Add staff form (name, email, Slack handle)
- [ ] Inline edit and delete per staff member
- [ ] TanStack Query hooks for all staff API calls
- [ ] Optimistic updates or refetch on mutation

---

## Phase 4 — Meeting Sessions API
> Goal: backend can create and manage meeting lifecycle

- [ ] `POST /meetings` — create new meeting, returns id
- [ ] `GET /meetings` — list all meetings with status
- [ ] `GET /meetings/{id}` — get single meeting with tasks
- [ ] `PATCH /meetings/{id}` — update status (recording → reviewing → sent)
- [ ] `POST /meetings/{id}/transcript` — append transcript chunk
- [ ] Meeting status enum: `recording | reviewing | sent`

---

## Phase 5 — Live Transcription
> Goal: mic audio is transcribed in real-time and streamed to the UI

- [ ] `services/transcription.py` loads `faster-whisper` model on startup
- [ ] Audio captured from mic in chunks (via browser `MediaRecorder` API)
- [ ] Frontend sends audio blobs to `POST /meetings/{id}/transcript/chunk`
- [ ] Backend transcribes chunk and appends to meeting transcript
- [ ] `GET /meetings/{id}/transcript/stream` SSE endpoint streams new text to frontend
- [ ] `MeetingPage` displays live rolling transcript via `EventSource`
- [ ] Start / Stop recording buttons update meeting status correctly

---

## Phase 6 — Task Extraction (Claude)
> Goal: Claude reads the transcript and returns a structured task list

- [ ] `services/extraction.py` contains `EXTRACTION_PROMPT` and extraction logic
- [ ] Prompt includes full transcript + staff roster (id, name)
- [ ] Uses Claude tool use or JSON mode to return structured output
- [ ] Response parsed into list of `{description, assignee_id, due_date, confidence}`
- [ ] `POST /meetings/{id}/extract` endpoint triggers extraction and saves tasks to DB
- [ ] Extraction triggered automatically when organizer stops recording
- [ ] Handles Claude API errors gracefully (returns partial results if any)

---

## Phase 7 — Task Review UI
> Goal: organizer can review, edit, and confirm tasks before sending

- [ ] After recording stops, `MeetingPage` transitions to review mode
- [ ] Task list rendered with description, assignee dropdown, optional due date
- [ ] Assignee dropdown populated from staff roster
- [ ] Organizer can edit task description inline
- [ ] Organizer can delete a task (remove false positives)
- [ ] Organizer can add a task manually
- [ ] "Confirm & Send" button triggers `POST /meetings/{id}/send`
- [ ] Low-confidence tasks visually flagged

---

## Phase 8 — Email Delivery
> Goal: confirmed tasks are emailed to each assignee

- [ ] `services/email.py` sends email via SMTP using env config
- [ ] Tasks batched by assignee — one email per person
- [ ] Email body: plain text list of assigned tasks with descriptions and due dates
- [ ] `POST /meetings/{id}/send` calls email service after saving tasks
- [ ] `sent_at` timestamp set on each task after successful send
- [ ] Failed sends logged; partial success handled without crashing

---

## Phase 9 — Task List View
> Goal: organizer can review all past meetings and their tasks

- [ ] `TaskListPage` lists all meetings (title, date, status, task count)
- [ ] Clicking a meeting shows its confirmed tasks and assignees
- [ ] Tasks grouped by assignee within a meeting
- [ ] Basic empty state for no meetings yet

---

## Phase 10 — Integration & Polish
> Goal: end-to-end flow works without errors; obvious rough edges smoothed

- [ ] Full end-to-end test: record → extract → review → send → verify email
- [ ] Loading states on all async operations
- [ ] Error messages shown to user on API failures
- [ ] `.env.example` is complete and accurate
- [ ] `README.md` updated with setup and run instructions
- [ ] CORS configured correctly for local dev
- [ ] No hardcoded localhost URLs in frontend (use env var for API base URL)

---

## Post-MVP Backlog

- [ ] Slack/Teams delivery
- [ ] User authentication
- [ ] Task status tracking (done / in progress)
- [ ] Export tasks to CSV or PDF
- [ ] Calendar integration
