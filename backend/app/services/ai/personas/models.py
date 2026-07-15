from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class PersonaType(str, Enum):
    HR = "hr_interviewer"
    SWE = "swe_interviewer"
    MLE = "mle_interviewer"
    PROFESSOR = "professor_interviewer"
    INVESTOR = "investor_interviewer"

class PersonaPromptContext(BaseModel):
    """Clean model wrapping persona data formatted for prompt construction."""
    persona_name: str = Field(description="Name of the interviewer persona.")
    persona_context: str = Field(description="Instruction context for the LLM system instructions.")

class Persona(BaseModel):
    """Strongly typed Pydantic model representing an interviewer persona."""
    id: PersonaType | str = Field(description="Unique identifier from PersonaType enum or custom string.")
    name: str = Field(min_length=1, description="Display name of the interviewer.")
    role: str = Field(min_length=1, description="Official role of the interviewer.")
    description: str = Field(min_length=1, description="High-level description of who they are.")
    interview_style: str = Field(min_length=1, description="Behavioral style of the interview (e.g., warm, analytical, precise).")
    supported_difficulty_levels: List[str] = Field(description="List of supported difficulty levels (e.g., junior, mid, senior).")
    focus_areas: List[str] = Field(description="Key technical or cultural areas they focus on.")
    system_context: str = Field(min_length=1, description="Prompt context instructing the LLM on this persona's behavior.")
