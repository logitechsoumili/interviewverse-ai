from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4


from sqlalchemy import DateTime, ForeignKey, JSON, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.evaluation import Evaluation
    from app.models.message import Message
    from app.models.persona import Persona
    from app.models.report import Report
    from app.models.user import User


class InterviewSession(Base):
    """An interview session owned by a user and driven by a persona."""

    __tablename__ = "interview_sessions"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    persona_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("personas.id", ondelete="RESTRICT"),
        nullable=False,
    )
    topics: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship(back_populates="interview_sessions")
    persona: Mapped[Persona] = relationship(back_populates="interview_sessions")
    messages: Mapped[list[Message]] = relationship(
        back_populates="interview_session",
        cascade="all, delete-orphan",
        order_by="Message.timestamp",
    )
    report: Mapped[Report | None] = relationship(
        back_populates="interview_session",
        cascade="all, delete-orphan",
        single_parent=True,
        uselist=False,
    )
    evaluation: Mapped[Evaluation | None] = relationship(
        back_populates="interview_session",
        cascade="all, delete-orphan",
        single_parent=True,
        uselist=False,
    )

