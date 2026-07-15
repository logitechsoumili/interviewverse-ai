"""Evaluation ORM model."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.interview_session import InterviewSession
    from app.models.user import User


class Evaluation(Base):
    """Evaluation generated for an interview session."""

    __tablename__ = "evaluations"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    session_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    overall_score: Mapped[int] = mapped_column(Integer, nullable=False)
    communication_score: Mapped[int] = mapped_column(Integer, nullable=False)
    technical_score: Mapped[int] = mapped_column(Integer, nullable=False)
    confidence_score: Mapped[int] = mapped_column(Integer, nullable=False)
    strengths: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    weaknesses: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    recommendations: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    learning_roadmap: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    evaluated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    interview_session: Mapped[InterviewSession] = relationship(back_populates="evaluation")
    user: Mapped[User] = relationship(back_populates="evaluations")
