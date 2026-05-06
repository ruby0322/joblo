from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from alignment_engine.api.schemas import AgentRunRequest, AgentRunResponse
from alignment_engine.db.repository import AgentRunRepository, UserRepository
from alignment_engine.db.session import get_session

router = APIRouter(tags=["Agents"])


@router.post("/agent/run", response_model=AgentRunResponse, status_code=status.HTTP_202_ACCEPTED)
def run_agent(payload: AgentRunRequest, session: Session = Depends(get_session)) -> AgentRunResponse:
    user_repo = UserRepository(session)
    run_repo = AgentRunRepository(session)
    user_repo.get_or_create_user(payload.user_id)
    run = run_repo.create_run(
        user_id=payload.user_id,
        run_type=payload.type,
        input_payload=payload.input,
        output_payload={"status": "queued"},
    )
    return AgentRunResponse(run_id=run.id, status="queued")
