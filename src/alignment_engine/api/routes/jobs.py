from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from alignment_engine.api.schemas import JobRecord, JobsIngestRequest, JobsIngestResponse
from alignment_engine.db.repository import JobRepository
from alignment_engine.db.session import get_session

router = APIRouter(tags=["Jobs"])


@router.post("/jobs/ingest", response_model=JobsIngestResponse)
def ingest_jobs(payload: JobsIngestRequest, session: Session = Depends(get_session)) -> JobsIngestResponse:
    job_repo = JobRepository(session)
    job_ids = []
    for job in payload.jobs:
        saved = job_repo.upsert_job(
            title=job.title,
            company=job.company,
            location=job.location,
            description=job.description,
            source=job.source,
            url=job.url,
            posted_at=job.posted_at,
        )
        job_ids.append(saved.id)
    return JobsIngestResponse(ingested_count=len(job_ids), job_ids=job_ids)


@router.get("/jobs")
def list_jobs(session: Session = Depends(get_session)) -> dict[str, list[JobRecord]]:
    job_repo = JobRepository(session)
    jobs = [JobRecord.model_validate(job) for job in job_repo.list_jobs()]
    return {"jobs": jobs}
