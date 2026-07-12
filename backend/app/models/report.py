"""Report ORM model."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Numeric, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.interview_session import InterviewSession


class Report(Base):
    """Evaluation report generated for an interview session."""

    __tablename__ = "reports"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    session_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    overall_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    communication_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    technical_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    confidence_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    feedback: Mapped[str] = mapped_column(Text, nullable=False)

    interview_session: Mapped[InterviewSession] = relationship(back_populates="report")
