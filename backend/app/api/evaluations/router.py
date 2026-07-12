from fastapi import APIRouter, Depends

from backend.app.services.ai.evaluation.service import EvaluationService
from backend.app.api.dependencies import get_evaluation_service
from backend.app.schemas.evaluations import EvaluationResponseSchema, EvaluationScoreSchema, EvaluationSummarySchema

router = APIRouter(prefix="/api/v1/interviews", tags=["Evaluations"])

@router.post("/{interview_id}/evaluate", response_model=EvaluationResponseSchema)
async def evaluate_interview(
    interview_id: str,
    service: EvaluationService = Depends(get_evaluation_service),
) -> EvaluationResponseSchema:
    """Orchestrates evaluation of a completed interview session."""
    evaluation = await service.evaluate_interview(interview_id)
    return EvaluationResponseSchema(
        scores=EvaluationScoreSchema(
            overall_score=evaluation.scores.overall_score,
            communication_score=evaluation.scores.communication_score,
            technical_score=evaluation.scores.technical_score,
            confidence_score=evaluation.scores.confidence_score,
        ),
        summary=EvaluationSummarySchema(
            strengths=evaluation.summary.strengths,
            weaknesses=evaluation.summary.weaknesses,
            recommendations=evaluation.summary.recommendations,
            learning_roadmap=evaluation.summary.learning_roadmap,
        ),
        evaluated_at=evaluation.evaluated_at,
        persona_id=evaluation.persona_id,
    )
