"""FastAPI application entrypoint for InterviewVerse AI."""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.api.exceptions import register_exception_handlers
from app.api import api_router
from app.core.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown events."""
    logger.info("InterviewVerse AI backend starting...")
    
    # Run database migrations programmatically on startup
    try:
        from alembic.config import Config
        from alembic import command
        import time
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        alembic_ini = os.path.normpath(os.path.join(current_dir, "..", "alembic.ini"))
        alembic_dir = os.path.normpath(os.path.join(current_dir, "..", "alembic"))
        
        logger.info(f"Loading Alembic config from {alembic_ini}")
        alembic_cfg = Config(alembic_ini)
        alembic_cfg.set_main_option("script_location", alembic_dir)
        alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url.replace("%", "%%"))
        
        # Run upgrade head with retries to handle database sleep/startup latency
        max_retries = 5
        retry_delay = 3
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Running database migrations (attempt {attempt}/{max_retries})...")
                command.upgrade(alembic_cfg, "head")
                logger.info("Database migrations upgraded successfully.")
                break
            except Exception as err:
                if attempt == max_retries:
                    raise err
                logger.warning(
                    f"Migration attempt {attempt} failed: {err}. Retrying in {retry_delay} seconds..."
                )
                time.sleep(retry_delay)
    except Exception as err:
        logger.error(f"Critical error running database migrations: {err}", exc_info=True)
        # Raise exception to fail fast in production if migrations cannot run
        raise err
        
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

    # Root metadata endpoint (prefixed with /api to avoid overriding frontend root)
    @app.get("/api", tags=["Metadata"])
    def get_metadata() -> dict:
        return {
            "title": app.title,
            "version": app.version,
            "description": "AI Interview Simulation Platform",
        }

    # Register aggregated API router (includes health, auth, and AI features)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)

    # Define paths to static build output
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.normpath(os.path.join(current_dir, "..", "..", "frontend", "out"))
    
    # Mount Next.js static asset directories for optimized serving
    next_static_dir = os.path.join(static_dir, "_next")
    if os.path.exists(next_static_dir):
        logger.info(f"Mounting Next.js static asset directory: {next_static_dir}")
        app.mount("/_next", StaticFiles(directory=next_static_dir), name="next_static")
    else:
        logger.warning(f"Next.js static assets not found at: {next_static_dir}. Make sure frontend is built.")

    @app.get("/{rest_of_path:path}", response_class=FileResponse)
    async def serve_static_or_spa(rest_of_path: str):
        # Normalize path
        normalized_path = rest_of_path.strip("/")
        
        # If it looks like an API route or docs route, return 404 instead of serving frontend
        if (
            normalized_path.startswith("api") 
            or normalized_path.startswith("docs")
            or normalized_path.startswith("redoc")
            or normalized_path == "openapi.json"
            or normalized_path == "health"
        ):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not Found")

        # Secure path containment check to prevent Directory Traversal LFI vulnerabilities
        abs_static_dir = os.path.abspath(static_dir)
        abs_file_path = os.path.abspath(os.path.join(static_dir, rest_of_path))
        try:
            if os.path.commonpath([abs_static_dir, abs_file_path]) != abs_static_dir:
                from fastapi import HTTPException
                raise HTTPException(status_code=403, detail="Forbidden")
        except ValueError:
            from fastapi import HTTPException
            raise HTTPException(status_code=403, detail="Forbidden")

        # 1. Check if the exact file exists (e.g. static assets, images, favicon)
        if os.path.isfile(abs_file_path):
            return FileResponse(abs_file_path)

        # Rewrite dynamic route paths to match Next.js static template output files
        # e.g., dashboard/interview/123 -> dashboard/interview/placeholder.html
        # e.g., dashboard/interview/123/evaluation -> dashboard/interview/placeholder/evaluation.html
        import re
        templated_path = normalized_path
        if re.match(r"^dashboard/interview/[^/]+$", normalized_path):
            templated_path = "dashboard/interview/placeholder"
        elif re.match(r"^dashboard/interview/[^/]+/evaluation$", normalized_path):
            templated_path = "dashboard/interview/placeholder/evaluation"
        elif re.match(r"^dashboard/interview/[^/]+/report$", normalized_path):
            templated_path = "dashboard/interview/placeholder/report"

        # 2. Check for page routes (e.g. /login -> serve login.html)
        if templated_path:
            html_file_path = os.path.join(static_dir, f"{templated_path}.html")
            if os.path.isfile(html_file_path):
                return FileResponse(html_file_path)

            # Check for folder/index.html (e.g. /login/ -> serve /login/index.html)
            index_file_path = os.path.join(static_dir, templated_path, "index.html")
            if os.path.isfile(index_file_path):
                return FileResponse(index_file_path)

        # 3. Fallback to index.html for SPA routing (e.g. root / or client-side routes)
        fallback_path = os.path.join(static_dir, "index.html")
        if os.path.isfile(fallback_path):
            return FileResponse(fallback_path)

        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not Found")

    return app


app = create_app()
