"""User ORM model."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.evaluation import Evaluation
    from app.models.interview_session import InterviewSession
    from app.models.persona import Persona
    from app.models.report import Report


class User(Base):
    """Application user who owns interview sessions."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    interview_sessions: Mapped[list[InterviewSession]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    personas: Mapped[list[Persona]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    evaluations: Mapped[list[Evaluation]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    reports: Mapped[list[Report]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

