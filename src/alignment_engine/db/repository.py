from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from alignment_engine.db.models import AgentRun, Job, JobMatch, Resume, ResumeVersion, User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_user(self, email: str) -> User:
        user = User(email=email)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user(self, user_id: UUID) -> User | None:
        return self.session.get(User, user_id)

    def get_or_create_user(self, user_id: UUID, email: str | None = None) -> User:
        existing = self.get_user(user_id)
        if existing is not None:
            return existing
        user = User(id=user_id, email=email or f"{user_id}@placeholder.local")
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user


class ResumeRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_resume(self, user_id: UUID, content: dict[str, Any], raw_text: str) -> Resume:
        resume = Resume(user_id=user_id, content=content, raw_text=raw_text)
        self.session.add(resume)
        self.session.commit()
        self.session.refresh(resume)
        return resume

    def get_latest_resume_for_user(self, user_id: UUID) -> Resume | None:
        stmt = (
            select(Resume)
            .where(Resume.user_id == user_id)
            .order_by(Resume.created_at.desc())
            .limit(1)
        )
        return self.session.scalar(stmt)


class JobRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert_job(
        self,
        *,
        title: str,
        company: str,
        location: str | None,
        description: str,
        source: str,
        url: str,
        posted_at: Any | None = None,
    ) -> Job:
        stmt = select(Job).where(Job.source == source, Job.url == url).limit(1)
        existing = self.session.scalar(stmt)
        if existing is None:
            job = Job(
                title=title,
                company=company,
                location=location,
                description=description,
                source=source,
                url=url,
                posted_at=posted_at,
            )
            self.session.add(job)
            self.session.commit()
            self.session.refresh(job)
            return job

        existing.title = title
        existing.company = company
        existing.location = location
        existing.description = description
        existing.posted_at = posted_at
        self.session.commit()
        self.session.refresh(existing)
        return existing

    def list_jobs(self) -> list[Job]:
        stmt = select(Job).order_by(Job.created_at.desc())
        return list(self.session.scalars(stmt))

    def get_job(self, job_id: UUID) -> Job | None:
        return self.session.get(Job, job_id)


class MatchRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert_match(
        self,
        *,
        user_id: UUID,
        job_id: UUID,
        score: float,
        explanation: dict[str, Any],
    ) -> JobMatch:
        stmt = select(JobMatch).where(JobMatch.user_id == user_id, JobMatch.job_id == job_id).limit(1)
        existing = self.session.scalar(stmt)
        if existing is None:
            match = JobMatch(
                user_id=user_id,
                job_id=job_id,
                match_score=score,
                explanation=explanation,
            )
            self.session.add(match)
            self.session.commit()
            self.session.refresh(match)
            return match

        existing.match_score = score
        existing.explanation = explanation
        self.session.commit()
        self.session.refresh(existing)
        return existing

    def get_match(self, *, user_id: UUID, job_id: UUID) -> JobMatch | None:
        stmt = select(JobMatch).where(JobMatch.user_id == user_id, JobMatch.job_id == job_id).limit(1)
        return self.session.scalar(stmt)


class ResumeVersionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_version(
        self,
        *,
        user_id: UUID,
        job_id: UUID,
        content: dict[str, Any],
        rationale: str,
    ) -> ResumeVersion:
        version = ResumeVersion(user_id=user_id, job_id=job_id, content=content, rationale=rationale)
        self.session.add(version)
        self.session.commit()
        self.session.refresh(version)
        return version


class AgentRunRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_run(
        self,
        *,
        user_id: UUID,
        run_type: str,
        input_payload: dict[str, Any],
        output_payload: dict[str, Any] | None = None,
    ) -> AgentRun:
        run = AgentRun(
            user_id=user_id,
            type=run_type,
            input=input_payload,
            output=output_payload or {},
        )
        self.session.add(run)
        self.session.commit()
        self.session.refresh(run)
        return run
