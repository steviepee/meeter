from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import StaffMember

router = APIRouter()


@router.get("", response_model=list[StaffMember])
def list_staff(session: Session = Depends(get_session)):
    return session.exec(select(StaffMember)).all()


@router.post("", response_model=StaffMember, status_code=201)
def create_staff(member: StaffMember, session: Session = Depends(get_session)):
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


@router.put("/{id}", response_model=StaffMember)
def update_staff(id: int, data: StaffMember, session: Session = Depends(get_session)):
    member = session.get(StaffMember, id)
    if not member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    member.name = data.name
    member.email = data.email
    member.slack_handle = data.slack_handle
    session.commit()
    session.refresh(member)
    return member


@router.delete("/{id}", status_code=204)
def delete_staff(id: int, session: Session = Depends(get_session)):
    member = session.get(StaffMember, id)
    if not member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    session.delete(member)
    session.commit()
