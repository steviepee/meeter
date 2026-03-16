# Meeter — Claude Code Instructions

## Project Overview

Meeter is a meeting-to-tasks application. It transcribes live meetings, uses Claude to extract action items, lets an organizer review and assign tasks, then emails them to staff.

See [PRD.md](PRD.md) for full product requirements.

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, SQLite (via SQLModel)
- **Frontend:** React 18, TypeScript, Vite, TailwindCSS, TanStack Query
- **AI:** Anthropic Claude API (`anthropic` Python SDK)
- **Transcription:** `faster-whisper` (local, real-time)
- **Email:** SMTP via Python `smtplib` or SendGrid

## Project Structure

```
meeter/
  backend/
    main.py           # FastAPI app entry point
    models.py         # SQLModel data models
    routes/
      meetings.py
      staff.py
    services/
      transcription.py  # Whisper integration
      extraction.py     # Claude task extraction
      email.py          # Email delivery
    database.py
  frontend/
    src/
      components/
      pages/
        MeetingPage.tsx
        TaskListPage.tsx
        SettingsPage.tsx
      api/              # TanStack Query hooks
    vite.config.ts
  PRD.md
  CLAUDE.md
```

## Development Setup

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Key Conventions

### Backend
- Use SQLModel for all DB models (combines SQLAlchemy + Pydantic)
- Route handlers stay thin — business logic lives in `services/`
- Transcription runs in a background thread; stream chunks to frontend via SSE
- Claude extraction prompt lives in `services/extraction.py` — keep it versioned and readable
- Store the Anthropic API key and SMTP credentials in a `.env` file (never commit it)

### Frontend
- One page per route: `MeetingPage`, `TaskListPage`, `SettingsPage`
- All API calls go through TanStack Query hooks in `src/api/`
- TailwindCSS only — no external component libraries for MVP
- Live transcript display uses SSE (`EventSource`)

### AI / Claude
- Task extraction uses `claude-sonnet-4-6` (latest capable model)
- Always pass the full staff roster in the extraction prompt so Claude can match names
- Return structured JSON via Claude's tool use or constrained output — do not parse freeform text
- Extraction prompt is in `services/extraction.py:EXTRACTION_PROMPT`

### Email
- Each confirmed task triggers one email per unique assignee (batch by person, not by task)
- Email template: plain text for MVP, list of tasks with descriptions

## Environment Variables

```
ANTHROPIC_API_KEY=
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM=
```

## What NOT to build (MVP scope)

- No authentication or user sessions
- No Slack integration (post-MVP)
- No task status updates after sending
- No multi-tenancy
- No calendar integrations
