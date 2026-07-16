from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from backend.app.services.ai.personas.models import PersonaType

class ReportSectionSchema(BaseModel):
    """Schema representing a structured narrative report section."""
    title: str = Field(description="Title of the section.")
    content: str = Field(description="Markdown or text content of the section.")

class ReportResponseSchema(BaseModel):
    """Response payload containing generated report details."""
    report_id: str = Field(description="Unique UUID report identifier.")
    interview_id: str = Field(description="Unique interview session identifier.")
    persona_id: PersonaType | str = Field(description="Persona ID of the interviewer.")
    generated_at: datetime = Field(description="Timestamp indicating when the report was generated.")
    executive_summary: ReportSectionSchema = Field(description="Concise narrative summary.")
    performance_overview: ReportSectionSchema = Field(description="Performance overview showing score metrics.")
    strengths: List[str] = Field(description="List of candidate strengths.")
    weaknesses: List[str] = Field(description="List of candidate weaknesses.")
    recommendations: List[str] = Field(description="List of candidate recommendations.")
    learning_roadmap: List[str] = Field(description="List of roadmap items.")
    markdown_report: str = Field(description="Fully rendered markdown export of the report.")
