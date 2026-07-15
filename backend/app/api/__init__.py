"""API router aggregation for InterviewVerse AI."""

from fastapi import APIRouter

from app.api.health import router as health_router
from app.auth.router import router as auth_router
from app.users.router import router as users_router

# AI Feature Routers from HEAD
from backend.app.api.personas.router import router as personas_router
from backend.app.api.interviews.router import router as interviews_router
from backend.app.api.evaluations.router import router as evaluations_router
from backend.app.api.reports.router import router as reports_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)


# Include AI Feature Routers
api_router.include_router(personas_router)
api_router.include_router(interviews_router)
api_router.include_router(evaluations_router)
api_router.include_router(reports_router)
