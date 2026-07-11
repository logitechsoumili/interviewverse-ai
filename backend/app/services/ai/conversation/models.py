from enum import Enum
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from backend.app.services.ai.personas.models import PersonaType

class SpeakerType(str, Enum):
    INTERVIEWER = "interviewer"
    CANDIDATE = "candidate"

class ConversationTurn(BaseModel):
    """Represents a single turn in the interview conversation."""
    role: SpeakerType = Field(description="The role of the speaker (interviewer/candidate).")
    content: str = Field(min_length=1, description="The content of the turn.")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Turn timestamp.")

class ConversationSession(BaseModel):
    """Represents an interview session state and history."""
    session_id: str = Field(min_length=1, description="Unique session identifier.")
    persona_id: PersonaType = Field(description="Interviewer persona identifier.")
    turns: List[ConversationTurn] = Field(default_factory=list, description="Chronological list of turns.")
    is_active: bool = Field(default=True, description="Indicates if the conversation session is active.")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Session creation timestamp.")
