import uuid
from datetime import datetime, timezone
from typing import List
from pydantic import BaseModel, Field, field_validator
from backend.app.services.ai.personas.models import PersonaType

class ReportSection(BaseModel):
    """Represents a structured section of the interview report."""
    title: str = Field(description="The title of the report section.")
    content: str = Field(description="The narrative content of the section.")

    @field_validator("title", "content")
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace-only.")
        return v.strip()

class ReportResult(BaseModel):
    """The final structured report result containing metadata, summaries, and markdown."""
    report_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique UUID4 report identifier."
    )
    interview_id: str = Field(description="Unique interview session identifier.")
    persona_id: PersonaType = Field(description="Persona ID of the interviewer.")
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp indicating when the report was generated (timezone-aware UTC)."
    )
    
    executive_summary: ReportSection = Field(description="Concise narrative summary.")
    performance_overview: ReportSection = Field(description="Structured performance overview showing score metrics.")
    
    strengths: List[str] = Field(description="List of candidate strengths.")
    weaknesses: List[str] = Field(description="List of candidate weaknesses.")
    recommendations: List[str] = Field(description="List of candidate recommendations.")
    learning_roadmap: List[str] = Field(description="List of roadmap items.")
    
    markdown_report: str = Field(description="Fully rendered markdown export.")

    @field_validator("report_id")
    @classmethod
    def validate_report_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("report_id is required and cannot be empty.")
        # Ensure it's a valid UUID
        try:
            uuid.UUID(v.strip())
        except ValueError as e:
            raise ValueError("report_id must be a valid UUID4.") from e
        return v.strip()

    @field_validator("markdown_report")
    @classmethod
    def validate_markdown_report(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("markdown_report cannot be empty.")
        return v.strip()
