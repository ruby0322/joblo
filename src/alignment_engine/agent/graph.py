from dataclasses import dataclass


@dataclass(frozen=True)
class AgentState:
    user_id: str
    job_id: str
    match_score: float | None = None
    next_action: str | None = None
    decision_reason: str | None = None


def run_decision_node(state: AgentState, threshold: float = 0.7) -> AgentState:
    score = state.match_score if state.match_score is not None else 0.0
    if score > threshold:
        return AgentState(
            user_id=state.user_id,
            job_id=state.job_id,
            match_score=score,
            next_action="resume_optimize",
            decision_reason="score_above_threshold",
        )

    return AgentState(
        user_id=state.user_id,
        job_id=state.job_id,
        match_score=score,
        next_action="discard_or_log",
        decision_reason="score_not_above_threshold",
    )
