from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from alignment_engine.api.schemas import ResumeOptimizeRequest, ResumeOptimizeResponse
from alignment_engine.db.repository import MatchRepository, ResumeVersionRepository
from alignment_engine.db.session import get_session

router = APIRouter(tags=["Matching"])


@router.post("/resume/optimize", response_model=ResumeOptimizeResponse)
def optimize_resume(
    payload: ResumeOptimizeRequest, session: Session = Depends(get_session)
) -> ResumeOptimizeResponse:
    # MVP behavior: require an existing match before optimization.
    match_repo = MatchRepository(session)
    version_repo = ResumeVersionRepository(session)
    existing = match_repo.get_match(user_id=payload.user_id, job_id=payload.job_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Run match before optimization",
        )

    overlap = existing.explanation.get("skill_overlap", [])
    missing = existing.explanation.get("missing_skills", [])
    summary = (
        "Reframed experience around overlap skills "
        f"{', '.join(overlap) if overlap else 'n/a'}; highlighted missing target "
        f"areas {', '.join(missing) if missing else 'n/a'}."
    )
    version = version_repo.create_version(
        user_id=payload.user_id,
        job_id=payload.job_id,
        content={"derived_from_match_id": str(existing.id)},
        rationale=summary,
    )
    return ResumeOptimizeResponse(resume_version_id=version.id, changes_summary=summary)
