from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from backend.app.services.ai.personas.models import PersonaType

class EvaluationScore(BaseModel):
    """Structured numeric scores for the candidate's performance."""
    overall_score: int = Field(ge=0, le=100, description="Overall score out of 100.")
    communication_score: int = Field(ge=0, le=100, description="Communication skills score out of 100.")
    technical_score: int = Field(ge=0, le=100, description="Technical skills score out of 100.")
    confidence_score: int = Field(ge=0, le=100, description="Confidence level score out of 100.")

class EvaluationSummary(BaseModel):
    """Qualitative feedback summary for the candidate."""
    strengths: List[str] = Field(description="Key candidate strengths observed.")
    weaknesses: List[str] = Field(description="Areas where the candidate can improve.")
    recommendations: List[str] = Field(description="Recommended next steps or decisions.")
    learning_roadmap: List[str] = Field(description="Targeted learning suggestions or roadmap steps.")

class EvaluationResult(BaseModel):
    """The final structured evaluation result containing metadata, scores, and summary."""
    scores: EvaluationScore = Field(description="Structured score metrics.")
    summary: EvaluationSummary = Field(description="Structured summary of the candidate assessment.")
    evaluated_at: datetime = Field(description="Timestamp indicating when the evaluation occurred.")
    persona_id: PersonaType | str = Field(description="Persona ID of the interviewer who conducted the session.")
