from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from backend.app.services.ai.personas.models import PersonaType

class EvaluationScoreSchema(BaseModel):
    """Schema representing numeric assessment scores."""
    overall_score: int = Field(ge=0, le=100, description="Overall score out of 100.")
    communication_score: int = Field(ge=0, le=100, description="Communication skills score out of 100.")
    technical_score: int = Field(ge=0, le=100, description="Technical skills score out of 100.")
    confidence_score: int = Field(ge=0, le=100, description="Confidence level score out of 100.")

class EvaluationSummarySchema(BaseModel):
    """Schema representing assessment qualitative summary text lists."""
    strengths: List[str] = Field(description="Observed candidate strengths.")
    weaknesses: List[str] = Field(description="Observed areas for improvement.")
    recommendations: List[str] = Field(description="Assessor recommendations.")
    learning_roadmap: List[str] = Field(description="Targeted learning roadmap suggestions.")

class EvaluationResponseSchema(BaseModel):
    """Response payload containing full evaluation results."""
    scores: EvaluationScoreSchema = Field(description="Structured score metrics.")
    summary: EvaluationSummarySchema = Field(description="Structured feedback summary.")
    evaluated_at: datetime = Field(description="Timestamp indicating when the evaluation occurred.")
    persona_id: PersonaType = Field(description="Interviewer persona ID.")
