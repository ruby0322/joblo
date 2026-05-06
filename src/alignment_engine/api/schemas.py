from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ResumeUploadRequest(BaseModel):
    user_id: UUID
    content: dict[str, Any]
    raw_text: str


class ResumeUploadResponse(BaseModel):
    resume_id: UUID


class ResumeRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    content: dict[str, Any]
    raw_text: str
    created_at: datetime


class JobIngestRecord(BaseModel):
    title: str
    company: str
    location: str | None = None
    description: str
    source: str
    url: str
    posted_at: datetime | None = None


class JobsIngestRequest(BaseModel):
    jobs: list[JobIngestRecord]


class JobsIngestResponse(BaseModel):
    ingested_count: int
    job_ids: list[UUID]


class JobRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    company: str
    location: str | None
    description: str
    source: str
    url: str
    posted_at: datetime | None
    created_at: datetime


class MatchRunRequest(BaseModel):
    user_id: UUID
    job_id: UUID


class MatchExplanation(BaseModel):
    skill_overlap: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    reasoning: str


class MatchRunResponse(BaseModel):
    score: float = Field(ge=0, le=1)
    reason: str
    explanation: MatchExplanation


class ResumeOptimizeRequest(BaseModel):
    user_id: UUID
    job_id: UUID


class ResumeOptimizeResponse(BaseModel):
    resume_version_id: UUID
    changes_summary: str


class AgentRunRequest(BaseModel):
    user_id: UUID
    type: Literal["manual", "cron"]
    input: dict[str, Any] = Field(default_factory=dict)


class AgentRunResponse(BaseModel):
    run_id: UUID
    status: Literal["queued", "running", "completed", "failed"]
