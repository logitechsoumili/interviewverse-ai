from fastapi import FastAPI
from backend.app.api.personas.router import router as personas_router
from backend.app.api.interviews.router import router as interviews_router
from backend.app.api.evaluations.router import router as evaluations_router
from backend.app.api.reports.router import router as reports_router
from backend.app.api.exceptions import register_exception_handlers

def create_app() -> FastAPI:
    """FastAPI application factory configuring metadata, routes, and exception handlers."""
    app = FastAPI(
        title="InterviewVerse AI",
        version="1.0.0",
        description="AI Interview Simulation Platform",
    )

    # Centralized exception handlers registration
    register_exception_handlers(app)

    # Root metadata endpoint
    @app.get("/", tags=["Metadata"])
    def get_metadata() -> dict:
        return {
            "title": app.title,
            "version": app.version,
            "description": app.description,
        }

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    def health_check() -> dict:
        return {"status": "ok"}

    # Register API routers
    app.include_router(personas_router)
    app.include_router(interviews_router)
    app.include_router(evaluations_router)
    app.include_router(reports_router)

    return app

app = create_app()
