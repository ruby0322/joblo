from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from alignment_engine.api.schemas import MatchExplanation, MatchRunRequest, MatchRunResponse
from alignment_engine.db.repository import JobRepository, MatchRepository, ResumeRepository
from alignment_engine.db.session import get_session
from alignment_engine.services.matching import compute_match

router = APIRouter(tags=["Matching"])


@router.post("/match/run", response_model=MatchRunResponse)
def run_match(payload: MatchRunRequest, session: Session = Depends(get_session)) -> MatchRunResponse:
    job_repo = JobRepository(session)
    resume_repo = ResumeRepository(session)
    match_repo = MatchRepository(session)

    job = job_repo.get_job(payload.job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    resume = resume_repo.get_latest_resume_for_user(payload.user_id)
    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    result = compute_match(resume.raw_text, job.description)
    explanation = {
        "skill_overlap": result.skill_overlap,
        "missing_skills": result.missing_skills,
        "reasoning": result.reasoning,
    }
    match_repo.upsert_match(
        user_id=payload.user_id,
        job_id=payload.job_id,
        score=result.score,
        explanation=explanation,
    )
    return MatchRunResponse(
        score=result.score,
        reason=result.reasoning,
        explanation=MatchExplanation(**explanation),
    )
