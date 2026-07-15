from datetime import datetime, timezone
import uuid
import hashlib
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.app.core.logging import StructuredLogger
from backend.app.services.ai.personas.service import PersonaService
from backend.app.services.ai.personas.models import PersonaType
from backend.app.services.ai.interview.repository import InterviewRepository
from backend.app.services.ai.interview.models import InterviewStatus
from backend.app.services.ai.interview.exceptions import InterviewNotFoundError
from backend.app.services.ai.evaluation.repository import EvaluationRepository
from backend.app.services.ai.evaluation.models import EvaluationResult
from backend.app.services.ai.reports.models import ReportSection, ReportResult
from backend.app.services.ai.reports.exceptions import (
    ReportError,
    ReportGenerationError,
    InvalidReportError,
)
from app.models.report import Report as ReportORM

def to_uuid(id_str: str) -> UUID:
    """Helper to convert string ID to UUID, with deterministic fallback for test strings."""
    try:
        return uuid.UUID(id_str)
    except ValueError:
        hex_digest = hashlib.md5(id_str.encode('utf-8')).hexdigest()
        return uuid.UUID(hex_digest)

class ReportService:
    """Deterministic Report Generation Engine with database persistence and user boundaries."""

    def __init__(
        self,
        interview_repository: InterviewRepository,
        persona_service: PersonaService,
        evaluation_repository: EvaluationRepository,
        db: Optional[Session] = None,
    ) -> None:
        """Initializes the ReportService with constructor-injected dependencies."""
        self.interview_repository = interview_repository
        self.persona_service = persona_service
        self.evaluation_repository = evaluation_repository
        self.db = db

    def _validate_non_empty(self, field_name: str, value: str) -> None:
        """Helper to reject empty or whitespace strings."""
        if not value or not value.strip():
            raise InvalidReportError(f"{field_name} cannot be empty or whitespace.")

    def build_executive_summary(
        self,
        evaluation_result: EvaluationResult,
        persona_name: str,
    ) -> ReportSection:
        """Generates a concise narrative summary derived only from existing evaluation data."""
        scores = evaluation_result.scores
        summary = evaluation_result.summary

        strengths_str = ", ".join(summary.strengths) if summary.strengths else "none highlighted"
        weaknesses_str = ", ".join(summary.weaknesses) if summary.weaknesses else "none highlighted"
        recs_str = ", ".join(summary.recommendations) if summary.recommendations else "none highlighted"

        content = (
            f"The candidate completed a technical interview conducted by {persona_name}. "
            f"Overall, they achieved a performance score of {scores.overall_score}/100. "
            f"The evaluation identified key strengths, specifically: {strengths_str}. "
            f"Additionally, the candidate could benefit from improvement in: {weaknesses_str}. "
            f"Based on the results, the recommendations are: {recs_str}."
        )

        return ReportSection(
            title="Executive Summary",
            content=content
        )

    def build_performance_overview(
        self,
        evaluation_result: EvaluationResult,
    ) -> ReportSection:
        """Generates a structured performance overview section showing scores."""
        scores = evaluation_result.scores

        content = (
            f"Overall Score: {scores.overall_score}/100\n"
            f"Technical Score: {scores.technical_score}/100\n"
            f"Communication Score: {scores.communication_score}/100\n"
            f"Confidence Score: {scores.confidence_score}/100"
        )

        return ReportSection(
            title="Performance Overview",
            content=content
        )

    def build_markdown_report(
        self,
        report: ReportResult,
    ) -> str:
        """Renders the ReportResult data structure into a formatted markdown string."""
        strengths_md = "\n".join(f"- {s}" for s in report.strengths) if report.strengths else "- None"
        weaknesses_md = "\n".join(f"- {w}" for w in report.weaknesses) if report.weaknesses else "- None"
        recs_md = "\n".join(f"- {r}" for r in report.recommendations) if report.recommendations else "- None"
        roadmap_md = "\n".join(f"- {lr}" for lr in report.learning_roadmap) if report.learning_roadmap else "- None"

        md_lines = [
            "# Interview Report",
            "",
            "## Executive Summary",
            "",
            report.executive_summary.content,
            "",
            "## Performance Overview",
            "",
            report.performance_overview.content,
            "",
            "## Strengths",
            "",
            strengths_md,
            "",
            "## Weaknesses",
            "",
            weaknesses_md,
            "",
            "## Recommendations",
            "",
            recs_md,
            "",
            "## Learning Roadmap",
            "",
            roadmap_md,
        ]
        return "\n".join(md_lines).strip()

    def generate_report(
        self,
        interview_id: str,
        user_id: Optional[UUID] = None,
    ) -> ReportResult:
        """Generates or retrieves a deterministic interview report enforcing user ownership."""
        self._validate_non_empty("Interview ID", interview_id)

        # 1. Retrieve interview & validate user ownership boundary
        try:
            if user_id is not None:
                interview = self.interview_repository.get_interview(interview_id, user_id=user_id)
            else:
                interview = self.interview_repository.get_interview(interview_id)
        except InterviewNotFoundError:
            raise
        except Exception as e:
            raise InvalidReportError(f"Interview session '{interview_id}' was not found.") from e

        # Validate that interview status is COMPLETED before generating the report
        if interview.status != InterviewStatus.COMPLETED:
            raise InvalidReportError(
                f"Cannot generate report for interview '{interview_id}' in state '{interview.status.value}'. "
                f"Interview must be in '{InterviewStatus.COMPLETED.value}' state."
            )

        # 2. Check if the report is already persisted in the database
        if self.db and user_id is not None:
            db_session_id = to_uuid(interview_id)
            stmt = select(ReportORM).where(ReportORM.session_id == db_session_id, ReportORM.user_id == user_id)
            db_report = self.db.execute(stmt).scalar_one_or_none()
            if db_report:
                return ReportResult(
                    report_id=str(db_report.id),
                    interview_id=str(db_report.session_id),
                    persona_id=PersonaType(interview.persona_id),
                    generated_at=db_report.generated_at,
                    executive_summary=ReportSection(
                        title=db_report.executive_summary.get("title", "Executive Summary"),
                        content=db_report.executive_summary.get("content", ""),
                    ),
                    performance_overview=ReportSection(
                        title=db_report.performance_overview.get("title", "Performance Overview"),
                        content=db_report.performance_overview.get("content", ""),
                    ),
                    strengths=db_report.strengths,
                    weaknesses=db_report.weaknesses,
                    recommendations=db_report.recommendations,
                    learning_roadmap=db_report.learning_roadmap,
                    markdown_report=db_report.markdown_report,
                )

        # 3. Retrieve evaluation & validate evaluation exists
        try:
            if user_id is not None:
                evaluation = self.evaluation_repository.get_evaluation(interview_id, user_id=user_id)
            else:
                evaluation = self.evaluation_repository.get_evaluation(interview_id)
        except Exception as e:
            raise InvalidReportError(f"Evaluation for interview '{interview_id}' was not found.") from e

        # 4. Retrieve persona context
        try:
            p_id = interview.persona_id.value if hasattr(interview.persona_id, 'value') else str(interview.persona_id)
            if user_id is not None:
                persona = self.persona_service.get_persona(p_id, user_id=user_id)
            else:
                persona = self.persona_service.get_persona(p_id)
        except Exception as e:
            raise ReportGenerationError(f"Failed to retrieve persona details: {str(e)}") from e

        StructuredLogger.info(
            "Generating deterministic interview report",
            extra={"interview_id": interview_id}
        )

        # 5. Build report sections
        try:
            exec_summary = self.build_executive_summary(evaluation, persona.name)
        except Exception as e:
            raise ReportGenerationError(f"Failed to build executive summary: {str(e)}") from e

        try:
            perf_overview = self.build_performance_overview(evaluation)
        except Exception as e:
            raise ReportGenerationError(f"Failed to build performance overview: {str(e)}") from e

        # 6. Construct ReportResult
        try:
            report_result = ReportResult(
                interview_id=interview_id,
                persona_id=interview.persona_id,
                executive_summary=exec_summary,
                performance_overview=perf_overview,
                strengths=evaluation.summary.strengths,
                weaknesses=evaluation.summary.weaknesses,
                recommendations=evaluation.summary.recommendations,
                learning_roadmap=evaluation.summary.learning_roadmap,
                markdown_report="Placeholder",
            )
        except Exception as e:
            raise InvalidReportError(f"Failed to construct ReportResult: {str(e)}") from e

        try:
            markdown_content = self.build_markdown_report(report_result)
            report_result.markdown_report = markdown_content
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate markdown report: {str(e)}") from e

        if not report_result.markdown_report.strip():
            raise InvalidReportError("Generated markdown report cannot be empty.")

        # 7. Persist generated report to database if DB is active
        if self.db and user_id is not None:
            db_report = ReportORM(
                id=to_uuid(report_result.report_id),
                session_id=to_uuid(interview_id),
                user_id=user_id,
                executive_summary={"title": exec_summary.title, "content": exec_summary.content},
                performance_overview={"title": perf_overview.title, "content": perf_overview.content},
                strengths=evaluation.summary.strengths,
                weaknesses=evaluation.summary.weaknesses,
                recommendations=evaluation.summary.recommendations,
                learning_roadmap=evaluation.summary.learning_roadmap,
                markdown_report=report_result.markdown_report,
                generated_at=report_result.generated_at,
            )
            self.db.add(db_report)
            self.db.commit()

        return report_result
