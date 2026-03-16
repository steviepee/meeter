from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select

from database import get_session
from models import Meeting, Task

router = APIRouter()


@router.post("", response_model=Meeting, status_code=201)
def create_meeting(meeting: Meeting, session: Session = Depends(get_session)):
    session.add(meeting)
    session.commit()
    session.refresh(meeting)
    return meeting


@router.get("", response_model=list[Meeting])
def list_meetings(session: Session = Depends(get_session)):
    return session.exec(select(Meeting)).all()


@router.get("/{id}", response_model=Meeting)
def get_meeting(id: int, session: Session = Depends(get_session)):
    meeting = session.get(Meeting, id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.get("/{id}/tasks", response_model=list[Task])
def get_meeting_tasks(id: int, session: Session = Depends(get_session)):
    meeting = session.get(Meeting, id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return session.exec(select(Task).where(Task.meeting_id == id)).all()


@router.patch("/{id}", response_model=Meeting)
def update_meeting_status(id: int, data: dict, session: Session = Depends(get_session)):
    meeting = session.get(Meeting, id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    if "status" in data:
        meeting.status = data["status"]
    session.commit()
    session.refresh(meeting)
    return meeting


@router.post("/{id}/transcript")
def append_transcript(id: int, data: dict, session: Session = Depends(get_session)):
    meeting = session.get(Meeting, id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    chunk = data.get("text", "")
    meeting.transcript = (meeting.transcript + " " + chunk).strip()
    session.commit()
    session.refresh(meeting)
    return {"transcript": meeting.transcript}


@router.post("/{id}/transcript/chunk")
async def transcribe_chunk_endpoint(id: int, request: Request, session: Session = Depends(get_session)):
    from services.transcription import transcribe_chunk
    meeting = session.get(Meeting, id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    audio_bytes = await request.body()
    text = transcribe_chunk(audio_bytes)
    meeting.transcript = (meeting.transcript + " " + text).strip()
    session.commit()
    session.refresh(meeting)
    return {"text": text, "transcript": meeting.transcript}


@router.post("/{id}/extract")
def extract_tasks_endpoint(id: int, session: Session = Depends(get_session)):
    from services.extraction import extract_tasks
    meeting = session.get(Meeting, id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    from models import StaffMember
    staff = [{"id": m.id, "name": m.name} for m in session.exec(select(StaffMember)).all()]
    tasks_data = extract_tasks(meeting.transcript, staff)
    saved = []
    for t in tasks_data:
        task = Task(
            meeting_id=id,
            description=t["description"],
            assignee_id=t.get("assignee_id"),
            due_date=t.get("due_date"),
        )
        session.add(task)
        saved.append(task)
    session.commit()
    for task in saved:
        session.refresh(task)
    return saved


@router.post("/{id}/send")
def send_tasks(id: int, data: dict, session: Session = Depends(get_session)):
    from services.email import send_tasks_email
    from models import StaffMember
    from datetime import datetime

    meeting = session.get(Meeting, id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    tasks_data = data.get("tasks", [])
    # Group by assignee_id
    by_assignee: dict[int | None, list] = {}
    for t in tasks_data:
        aid = t.get("assignee_id")
        by_assignee.setdefault(aid, []).append(t)

    errors = []
    for assignee_id, assignee_tasks in by_assignee.items():
        if assignee_id is None:
            continue
        member = session.get(StaffMember, assignee_id)
        if not member:
            continue
        try:
            send_tasks_email(
                {"id": member.id, "name": member.name, "email": member.email},
                assignee_tasks,
            )
        except Exception as exc:
            errors.append(str(exc))

    # Save tasks with sent_at
    now = datetime.utcnow()
    for t in tasks_data:
        task = Task(
            meeting_id=id,
            description=t["description"],
            assignee_id=t.get("assignee_id"),
            due_date=t.get("due_date"),
            sent_at=now if t.get("assignee_id") else None,
        )
        session.add(task)
    meeting.status = "sent"
    session.commit()

    return {"ok": True, "errors": errors}


@router.get("/{id}/transcript/stream")
def transcript_stream(id: int, session: Session = Depends(get_session)):
    meeting = session.get(Meeting, id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    transcript = meeting.transcript

    def event_stream():
        yield f"data: {transcript}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
