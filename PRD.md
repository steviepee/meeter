# Meeter — Product Requirements Document

## Overview

Meeter turns live meeting conversations into assigned, actionable tasks. It transcribes audio in real-time, uses an LLM to extract tasks with suggested assignees, lets the organizer review and confirm assignments, then delivers tasks to staff via email and an in-app task list.

---

## Problem Statement

After meetings, action items are frequently lost, misremembered, or unevenly distributed. Teams rely on someone manually writing notes and following up. Meeter automates this: the meeting itself becomes the input, and confirmed tasks become the output.

---

## Users

- **Organizer** — runs the meeting, reviews AI-suggested tasks, confirms and sends them
- **Staff members** — receive their assigned tasks via email; visible in the in-app task list
- Team size: 2–10 people
- No authentication required for MVP

---

## Core User Flow

1. Organizer opens Meeter and starts a new meeting session
2. Live audio from the microphone is transcribed in real-time and displayed on screen
3. When the meeting ends, the organizer stops the session
4. The AI (Claude) processes the full transcript and returns a list of extracted tasks, each with:
   - Task description
   - Suggested assignee (matched against the staff roster)
   - Optional due date (if mentioned)
5. Organizer reviews the task list, edits descriptions/assignees as needed, removes false positives
6. Organizer confirms — tasks are saved to the in-app list and emails are sent to each assignee

---

## Features

### MVP

| Feature | Description |
|---|---|
| Live transcription | Real-time mic audio → text using Whisper |
| Task extraction | Claude API processes transcript, returns structured task list |
| Review UI | Organizer edits tasks and assignees before confirming |
| In-app task list | All confirmed tasks stored and viewable per meeting |
| Email delivery | Each staff member receives their assigned tasks via email |
| Staff roster | Settings page: name, email, Slack handle per staff member |

### Post-MVP

- Slack/Teams message delivery
- Authentication (per-user accounts)
- Task status tracking (done/in progress)
- Calendar integration for meeting context
- Export to PDF or CSV

---

## Technical Architecture

### Backend — Python / FastAPI

- `POST /meetings` — create a new meeting session
- `POST /meetings/{id}/transcript` — append transcription chunks (streaming)
- `POST /meetings/{id}/extract` — trigger AI task extraction on full transcript
- `GET /meetings/{id}/tasks` — retrieve extracted task list
- `PUT /meetings/{id}/tasks` — update tasks after organizer review
- `POST /meetings/{id}/send` — confirm and deliver tasks (email + save)
- `GET /staff` — list staff roster
- `POST /staff` — add staff member
- `PUT /staff/{id}` — update staff member
- `DELETE /staff/{id}` — remove staff member

**Key dependencies:**
- `openai-whisper` or `faster-whisper` — transcription
- `anthropic` — Claude API for task extraction
- `fastapi`, `uvicorn` — web framework
- `sqlmodel` or `sqlite3` — lightweight local storage (MVP)
- `smtplib` / SendGrid SDK — email delivery

### Frontend — React / TypeScript

- **Meeting view** — start/stop session, live transcript display, task review UI
- **Task list view** — all meetings + confirmed tasks
- **Settings view** — staff roster management (name, email, Slack handle)

**Key dependencies:**
- `vite` — build tool
- `react`, `typescript`
- `tanstack/react-query` — data fetching
- `tailwindcss` — styling

### AI — Claude API

Prompt approach: send the full transcript with the staff roster and instruct Claude to return a structured JSON array of tasks. Each task includes:
```json
{
  "description": "string",
  "assignee_id": "string | null",
  "due_date": "ISO8601 | null",
  "confidence": "high | medium | low"
}
```

---

## Data Model

### Meeting
- `id`, `title`, `created_at`, `status` (recording | reviewing | sent)
- `transcript` (full text)
- `tasks` (list of Task)

### Task
- `id`, `meeting_id`, `description`, `assignee_id`, `due_date`, `sent_at`

### StaffMember
- `id`, `name`, `email`, `slack_handle`

---

## Out of Scope (MVP)

- Multi-tenant / org isolation
- User authentication
- Slack delivery
- Mobile app
- Recurring meeting detection
- Task completion tracking

---

## Success Criteria (MVP)

- A meeting can be transcribed end-to-end from mic to text
- Claude extracts at least 80% of clearly stated action items from a test transcript
- Organizer can review, edit, and confirm tasks in under 2 minutes
- Confirmed tasks are emailed to the correct staff members
- Staff roster can be created and edited in settings
