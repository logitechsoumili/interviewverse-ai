from fastapi import APIRouter, Depends

from backend.app.services.ai.reports.service import ReportService
from backend.app.api.dependencies import get_report_service
from backend.app.schemas.reports import ReportResponseSchema, ReportSectionSchema

router = APIRouter(prefix="/api/v1/interviews", tags=["Reports"])

@router.get("/{interview_id}/report", response_model=ReportResponseSchema)
def get_report(
    interview_id: str,
    service: ReportService = Depends(get_report_service),
) -> ReportResponseSchema:
    """Generates a deterministic interview report."""
    report = service.generate_report(interview_id)
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
