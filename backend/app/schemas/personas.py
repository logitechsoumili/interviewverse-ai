from pydantic import BaseModel, Field
from typing import List, Optional

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

class PersonaCreateSchema(BaseModel):
    """Schema representing creation request payload for custom personas."""
    id: str = Field(description="Unique string identifier for the custom persona.")
    name: str = Field(min_length=1, description="Display name of the interviewer.")
    role: str = Field(min_length=1, description="Official role of the interviewer.")
    description: str = Field(min_length=1, description="High-level description of who they are.")
    interview_style: str = Field(min_length=1, description="Behavioral style of the interview.")
    supported_difficulty_levels: List[str] = Field(description="List of supported difficulty levels.")
    focus_areas: List[str] = Field(description="Key technical or cultural areas they focus on.")
    system_context: str = Field(min_length=1, description="Prompt context instructing the LLM.")

class PersonaUpdateSchema(BaseModel):
    """Schema representing update request payload for custom personas."""
    name: Optional[str] = Field(None, min_length=1)
    role: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, min_length=1)
    interview_style: Optional[str] = Field(None, min_length=1)
    supported_difficulty_levels: Optional[List[str]] = Field(None)
    focus_areas: Optional[List[str]] = Field(None)
    system_context: Optional[str] = Field(None, min_length=1)
