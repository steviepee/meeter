from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class StaffMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    slack_handle: Optional[str] = None


class Meeting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "recording"
    transcript: str = ""


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    meeting_id: int = Field(foreign_key="meeting.id")
    description: str
    assignee_id: Optional[int] = None
    due_date: Optional[str] = None
    sent_at: Optional[datetime] = None
