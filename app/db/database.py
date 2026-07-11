"""SQLAlchemy engine configuration for InterviewVerse AI."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.core.config import settings


def _create_engine() -> Engine:
    """Create the application's SQLAlchemy engine."""
    engine_kwargs: dict[str, object] = {
        "echo": settings.debug,
        "future": True,
    }

    if settings.database_url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    else:
        engine_kwargs["pool_pre_ping"] = True
        engine_kwargs["pool_recycle"] = 300

    return create_engine(settings.database_url, **engine_kwargs)


engine: Engine = _create_engine()
