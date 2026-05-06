from __future__ import annotations

from fastapi import FastAPI

from alignment_engine.api.routes.agent import router as agent_router
from alignment_engine.api.routes.jobs import router as jobs_router
from alignment_engine.api.routes.match import router as match_router
from alignment_engine.api.routes.optimize import router as optimize_router
from alignment_engine.api.routes.resume import router as resume_router
from alignment_engine.db.session import init_db


def create_app() -> FastAPI:
    init_db()
    app = FastAPI(
        title="Job-to-Candidate Alignment Engine API",
        version="0.1.0",
        description="MVP API for matching and resume optimization",
    )
    app.include_router(resume_router)
    app.include_router(jobs_router)
    app.include_router(match_router)
    app.include_router(optimize_router)
    app.include_router(agent_router)
    return app


app = create_app()
