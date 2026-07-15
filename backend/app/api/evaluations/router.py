from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.services.ai.evaluation.service import EvaluationService
from backend.app.api.dependencies import get_evaluation_service, get_current_user
from backend.app.schemas.evaluations import EvaluationResponseSchema, EvaluationScoreSchema, EvaluationSummarySchema
from backend.app.services.ai.evaluation.exceptions import (
    EvaluationNotFoundError,
    InvalidEvaluationError,
    EvaluationParsingError,
    EvaluationError,
)
from app.models.user import User

router = APIRouter(prefix="/api/v1/interviews", tags=["Evaluations"])

@router.post("/{interview_id}/evaluate", response_model=EvaluationResponseSchema)
async def evaluate_interview(
    interview_id: str,
    service: EvaluationService = Depends(get_evaluation_service),
    current_user: User = Depends(get_current_user),
) -> EvaluationResponseSchema:
    """Orchestrates evaluation of a completed interview session, enforcing user ownership."""
    try:
        evaluation = await service.evaluate_interview(interview_id, user_id=current_user.id)
    except EvaluationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found."
        )
    except InvalidEvaluationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except (EvaluationParsingError, EvaluationError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
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
