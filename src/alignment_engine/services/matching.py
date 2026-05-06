from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class MatchComputation:
    score: float
    skill_overlap: list[str]
    missing_skills: list[str]
    reasoning: str


def _tokenize(text: str) -> set[str]:
    tokens = re.findall(r"[a-zA-Z0-9+#.-]+", text.lower())
    return {token for token in tokens if len(token) > 1}


def compute_match(resume_text: str, job_description: str) -> MatchComputation:
    resume_tokens = _tokenize(resume_text)
    job_tokens = _tokenize(job_description)

    overlap = sorted(resume_tokens & job_tokens)
    missing = sorted(job_tokens - resume_tokens)
    denominator = max(1, len(job_tokens))
    score = round(min(1.0, len(overlap) / denominator), 4)

    reasoning = (
        f"Overlap on {len(overlap)} keywords; missing {len(missing)} job keywords. "
        "This is a deterministic baseline score for MVP."
    )
    return MatchComputation(
        score=score,
        skill_overlap=overlap[:15],
        missing_skills=missing[:15],
        reasoning=reasoning,
    )
