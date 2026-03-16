# Meeter

A meeting-to-tasks application. Records meetings, transcribes audio in real-time using Whisper, extracts action items via Claude, lets you review and assign tasks, then emails them to staff.

## Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env if your backend runs on a different port
npm run dev
```

Open http://localhost:5173

## Environment Variables

**backend/.env**

```
ANTHROPIC_API_KEY=sk-...
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASSWORD=secret
SMTP_FROM=noreply@example.com
```

**frontend/.env**

```
VITE_API_BASE_URL=http://localhost:8000
```

## Running Tests

```bash
cd backend
pytest -v
```

## Usage

1. Go to **Settings** and add your staff members (name, email, optional Slack handle).
2. Go to **Meeting** and click **Start Recording** — your microphone will be captured and transcribed live.
3. Click **Stop Recording** — Claude will extract action items automatically.
4. Review the extracted tasks: edit descriptions, assign to staff, set due dates, delete false positives, or add missing tasks.
5. Click **Confirm & Send** — each assigned staff member receives an email with their tasks.
6. Go to **All Meetings** to review past meetings and their tasks.
