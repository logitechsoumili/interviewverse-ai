from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.services.ai.reports.service import ReportService
from backend.app.api.dependencies import get_report_service, get_current_user
from backend.app.schemas.reports import ReportResponseSchema, ReportSectionSchema
from backend.app.services.ai.reports.exceptions import (
    InvalidReportError,
    ReportGenerationError,
)
from backend.app.services.ai.interview.exceptions import InterviewNotFoundError
from app.models.user import User

router = APIRouter(prefix="/api/v1/interviews", tags=["Reports"])

@router.get("/{interview_id}/report", response_model=ReportResponseSchema)
def get_report(
    interview_id: str,
    service: ReportService = Depends(get_report_service),
    current_user: User = Depends(get_current_user),
) -> ReportResponseSchema:
    """Generates a deterministic interview report, enforcing user ownership boundaries."""
    try:
        report = service.generate_report(interview_id, user_id=current_user.id)
    except InterviewNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidReportError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ReportGenerationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    return ReportResponseSchema(
        report_id=report.report_id,
        interview_id=report.interview_id,
        persona_id=report.persona_id,
        generated_at=report.generated_at,
        executive_summary=ReportSectionSchema(
            title=report.executive_summary.title,
            content=report.executive_summary.content,
        ),
        performance_overview=ReportSectionSchema(
            title=report.performance_overview.title,
            content=report.performance_overview.content,
        ),
        strengths=report.strengths,
        weaknesses=report.weaknesses,
        recommendations=report.recommendations,
        learning_roadmap=report.learning_roadmap,
        markdown_report=report.markdown_report,
    )
