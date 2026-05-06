from __future__ import annotations

from uuid import UUID

from alignment_engine.agent.flow import MatchResult, build_resume_optimizer_payload


def build_optimization_result(
    *,
    user_id: UUID,
    job_id: UUID,
    score: float,
    skill_overlap: list[str],
    missing_skills: list[str],
    reasoning: str,
) -> dict[str, object]:
    payload = build_resume_optimizer_payload(
        user_id=str(user_id),
        job_id=str(job_id),
        match_result=MatchResult(
            score=score,
            skill_overlap=skill_overlap,
            missing_skills=missing_skills,
            reasoning=reasoning,
        ),
    )
    return payload
