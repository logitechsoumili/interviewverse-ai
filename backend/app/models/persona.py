"""Persona ORM model."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID


from sqlalchemy import ForeignKey, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.interview_session import InterviewSession
    from app.models.user import User


class Persona(Base):
    """Interview persona used to shape a session."""

    __tablename__ = "personas"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    interview_style: Mapped[str] = mapped_column(String(255), nullable=False)
    supported_difficulty_levels: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    focus_areas: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    system_context: Mapped[str] = mapped_column(Text, nullable=False)

    interview_sessions: Mapped[list[InterviewSession]] = relationship(
        back_populates="persona",
    )
    user: Mapped[User] = relationship(back_populates="personas")

