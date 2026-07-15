from pydantic import BaseModel, Field
from typing import List

class PersonaListItemSchema(BaseModel):
    """Schema representing a summarized persona for lists."""
    id: str = Field(description="Unique identifier from PersonaType enum.")
    name: str = Field(description="Display name of the interviewer.")
    role: str = Field(description="Official role of the interviewer.")

class PersonaDetailSchema(BaseModel):
    """Schema representing detailed persona fields."""
    id: str = Field(description="Unique identifier from PersonaType enum.")
    name: str = Field(description="Display name of the interviewer.")
    role: str = Field(description="Official role of the interviewer.")
    description: str = Field(description="High-level description of who they are.")
    interview_style: str = Field(description="Behavioral style of the interview.")
    supported_difficulty_levels: List[str] = Field(description="List of supported difficulty levels.")
    focus_areas: List[str] = Field(description="Key technical or cultural areas they focus on.")
