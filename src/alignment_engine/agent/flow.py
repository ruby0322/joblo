from dataclasses import dataclass


@dataclass(frozen=True)
class MatchResult:
    score: float
    skill_overlap: list[str]
    missing_skills: list[str]
    reasoning: str


def should_trigger_resume_optimizer(score: float, threshold: float = 0.7) -> bool:
    return score > threshold


def build_resume_optimizer_payload(
    user_id: str,
    job_id: str,
    match_result: MatchResult,
) -> dict[str, object]:
    overlap = ", ".join(match_result.skill_overlap) if match_result.skill_overlap else "n/a"
    missing = ", ".join(match_result.missing_skills) if match_result.missing_skills else "n/a"

    return {
        "user_id": user_id,
        "job_id": job_id,
        "match_score": match_result.score,
        "changes_summary": (
            "Highlight overlap skills: "
            f"{overlap}. Address missing focus areas: {missing}."
        ),
        "constraints": {
            "invent_experience": False,
            "allowed_actions": ["reframe", "reorder", "highlight_keywords"],
        },
        "reasoning": match_result.reasoning,
    }
