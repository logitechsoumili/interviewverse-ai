from enum import Enum
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field
from backend.app.services.ai.personas.models import PersonaType

class InterviewStatus(str, Enum):
    STARTING = "starting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class InterviewTurnResult(BaseModel):
    """Result of a single turn in the technical interview."""
    question: str = Field(min_length=1, description="The interview question generated for this turn.")
    is_final: bool = Field(default=False, description="Flag indicating if the interview is completed.")
    turn_count: int = Field(ge=0, description="Total number of turns completed so far.")

class InterviewSession(BaseModel):
    """Represents a technical interview orchestration session."""
    interview_id: str = Field(min_length=1, description="Unique identifier for the interview.")
    session_id: str = Field(min_length=1, description="Conversation session identifier.")
    persona_id: PersonaType = Field(description="The persona identifier.")
    status: InterviewStatus = Field(default=InterviewStatus.STARTING, description="Current interview status.")
    topics: List[str] = Field(description="Focus areas/topics for this interview.")
    difficulty: str = Field(min_length=1, description="Target difficulty level.")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Creation timestamp.")
    completed_at: Optional[datetime] = Field(default=None, description="Completion timestamp.")
