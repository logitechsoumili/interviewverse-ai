
"""API router aggregation for InterviewVerse AI."""

from fastapi import APIRouter

from backend.app.api.health import router as health_router
from backend.app.auth.router import router as auth_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
