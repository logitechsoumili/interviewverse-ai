from datetime import datetime, timezone
import uuid
from typing import List, Optional

from backend.app.core.logging import StructuredLogger
from backend.app.services.ai.personas.service import PersonaService
from backend.app.services.ai.interview.repository import InterviewRepository
from backend.app.services.ai.interview.models import InterviewStatus
from backend.app.services.ai.evaluation.repository import EvaluationRepository
from backend.app.services.ai.evaluation.models import EvaluationResult
from backend.app.services.ai.reports.models import ReportSection, ReportResult
from backend.app.services.ai.reports.exceptions import (
    ReportError,
    ReportGenerationError,
    InvalidReportError,
)

class ReportService:
    """Deterministic Report Generation Engine.
    
    Synthesizes and formats completed interview evaluations into structured markdown reports.
    """

    def __init__(
        self,
        interview_repository: InterviewRepository,
        persona_service: PersonaService,
        evaluation_repository: EvaluationRepository,
    ) -> None:
        """Initializes the ReportService with constructor-injected dependencies.
        
        Args:
            interview_repository: Injected InterviewRepository.
            persona_service: Injected PersonaService.
            evaluation_repository: Injected EvaluationRepository.
        """
        self.interview_repository = interview_repository
        self.persona_service = persona_service
        self.evaluation_repository = evaluation_repository

    def _validate_non_empty(self, field_name: str, value: str) -> None:
        """Helper to reject empty or whitespace strings."""
        if not value or not value.strip():
            raise InvalidReportError(f"{field_name} cannot be empty or whitespace.")

    def build_executive_summary(
        self,
        evaluation_result: EvaluationResult,
        persona_name: str,
    ) -> ReportSection:
        """Generates a concise narrative summary derived only from existing evaluation data.
        
        Args:
            evaluation_result: The source EvaluationResult.
            persona_name: Display name of the interviewer persona.
            
        Returns:
            A ReportSection representing the Executive Summary.
        """
        scores = evaluation_result.scores
        summary = evaluation_result.summary

        # Build a strict, deterministic narrative synthesis
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
        """Generates a structured performance overview section showing scores.
        
        Args:
            evaluation_result: The source EvaluationResult.
            
        Returns:
            A ReportSection representing the Performance Overview.
        """
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
        """Renders the ReportResult data structure into a formatted markdown string.
        
        Args:
            report: The ReportResult containing the structured data.
            
        Returns:
            The fully rendered markdown report string.
        """
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
    ) -> ReportResult:
        """Generates a deterministic interview report.
        
        Args:
            interview_id: Unique identifier for the interview session.
            
        Returns:
            The generated ReportResult.
            
        Raises:
            InvalidReportError: If validations fail (empty ID, missing interview, missing evaluation).
            ReportGenerationError: If formatting or construction fails.
        """
        # 1. Validate interview ID
        self._validate_non_empty("Interview ID", interview_id)

        # 2. Retrieve interview & 3. Validate interview exists
        try:
            interview = self.interview_repository.get_interview(interview_id)
        except Exception as e:
            raise InvalidReportError(f"Interview session '{interview_id}' was not found.") from e

        # Validate that interview status is COMPLETED before generating the report
        if interview.status != InterviewStatus.COMPLETED:
            raise InvalidReportError(
                f"Cannot generate report for interview '{interview_id}' in state '{interview.status.value}'. "
                f"Interview must be in '{InterviewStatus.COMPLETED.value}' state."
            )

        # 4. Retrieve evaluation & 5. Validate evaluation exists
        try:
            evaluation = self.evaluation_repository.get_evaluation(interview_id)
        except Exception as e:
            raise InvalidReportError(f"Evaluation for interview '{interview_id}' was not found.") from e

        # 6. Retrieve persona
        try:
            persona = self.persona_service.get_persona(interview.persona_id)
        except Exception as e:
            raise ReportGenerationError(f"Failed to retrieve persona details: {str(e)}") from e

        StructuredLogger.info(
            "Generating deterministic interview report",
            extra={"interview_id": interview_id}
        )

        # 7. Build executive summary
        try:
            exec_summary = self.build_executive_summary(evaluation, persona.name)
        except Exception as e:
            raise ReportGenerationError(f"Failed to build executive summary: {str(e)}") from e

        # 8. Build performance overview
        try:
            perf_overview = self.build_performance_overview(evaluation)
        except Exception as e:
            raise ReportGenerationError(f"Failed to build performance overview: {str(e)}") from e

        # 9. Construct ReportResult (using Pydantic default factories for report_id and generated_at)
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
                markdown_report="Placeholder",  # Temp string to pass Pydantic validation
            )
        except Exception as e:
            raise InvalidReportError(f"Failed to construct ReportResult: {str(e)}") from e

        # 10. Generate markdown export
        try:
            markdown_content = self.build_markdown_report(report_result)
            report_result.markdown_report = markdown_content
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate markdown report: {str(e)}") from e

        # Validate that markdown output is not empty
        if not report_result.markdown_report.strip():
            raise InvalidReportError("Generated markdown report cannot be empty.")

        # 11. Return ReportResult
        return report_result
