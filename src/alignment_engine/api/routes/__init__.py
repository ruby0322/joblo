from .agent import router as agent_router
from .jobs import router as jobs_router
from .match import router as match_router
from .optimize import router as optimize_router
from .resume import router as resume_router

__all__ = [
    "agent_router",
    "jobs_router",
    "match_router",
    "optimize_router",
    "resume_router",
]
