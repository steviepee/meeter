# Claude extraction — Phase 6
import os
import json
import anthropic

EXTRACTION_PROMPT = """You are an assistant that extracts action items from meeting transcripts.

Given the meeting transcript and staff roster below, identify all action items mentioned.
For each action item, determine who it's assigned to (if mentioned), when it's due (if mentioned),
and how confident you are (0.0 to 1.0).

Staff roster:
{staff_roster}

Meeting transcript:
{transcript}

Return a JSON array of tasks. Each task must have:
- description: string — the action item
- assignee_id: integer or null — the staff member's id, or null if unassigned
- due_date: string or null — ISO date string (YYYY-MM-DD) or null
- confidence: float — 0.0 to 1.0
"""

_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    return _client


def extract_tasks(transcript: str, staff: list) -> list[dict]:
    roster = "\n".join(f"- id={m['id']}, name={m['name']}" for m in staff)
    prompt = EXTRACTION_PROMPT.format(staff_roster=roster, transcript=transcript)

    client = _get_client()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=[
            {
                "name": "save_tasks",
                "description": "Save extracted tasks from the meeting transcript",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tasks": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "description": {"type": "string"},
                                    "assignee_id": {"type": ["integer", "null"]},
                                    "due_date": {"type": ["string", "null"]},
                                    "confidence": {"type": "number"},
                                },
                                "required": ["description", "assignee_id", "due_date", "confidence"],
                            },
                        }
                    },
                    "required": ["tasks"],
                },
            }
        ],
        tool_choice={"type": "tool", "name": "save_tasks"},
        messages=[{"role": "user", "content": prompt}],
    )

    for block in message.content:
        if block.type == "tool_use" and block.name == "save_tasks":
            return block.input.get("tasks", [])

    return []
