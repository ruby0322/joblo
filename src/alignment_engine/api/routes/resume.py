from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from alignment_engine.api.schemas import ResumeRecord, ResumeUploadRequest, ResumeUploadResponse
from alignment_engine.db.repository import ResumeRepository, UserRepository
from alignment_engine.db.session import get_session

router = APIRouter(tags=["Resume"])


@router.post("/resume/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
def upload_resume(payload: ResumeUploadRequest, session: Session = Depends(get_session)) -> ResumeUploadResponse:
    user_repo = UserRepository(session)
    resume_repo = ResumeRepository(session)
    user_repo.get_or_create_user(payload.user_id)
    created = resume_repo.create_resume(
        user_id=payload.user_id,
        content=payload.content,
        raw_text=payload.raw_text,
    )
    return ResumeUploadResponse(resume_id=created.id)


@router.get("/resume/{user_id}", response_model=ResumeRecord)
def get_resume(user_id: UUID, session: Session = Depends(get_session)) -> ResumeRecord:
    resume_repo = ResumeRepository(session)
    resume = resume_repo.get_latest_resume_for_user(user_id=user_id)
    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    return ResumeRecord.model_validate(resume)
