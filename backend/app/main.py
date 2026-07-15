"""FastAPI application entrypoint for InterviewVerse AI."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from backend.app.api.exceptions import register_exception_handlers
from app.api import api_router
from app.core.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown events."""
    logger.info("InterviewVerse AI backend starting...")
    yield


def create_app() -> FastAPI:
    """FastAPI application factory configuring metadata, routes, and exception handlers."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Centralized exception handlers registration from HEAD
    register_exception_handlers(app)

    # Root metadata endpoint
    @app.get("/", tags=["Metadata"])
    def get_metadata() -> dict:
        return {
            "title": app.title,
            "version": app.version,
            "description": "AI Interview Simulation Platform",
        }

    # Register aggregated API router (includes health, auth, and AI features)
    app.include_router(api_router)

    return app


app = create_app()
