# pyrefly: ignore [missing-import]
import pytest
import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock

from backend.app.services.ai.personas.models import Persona, PersonaType
from backend.app.services.ai.interview.models import InterviewSession, InterviewStatus
from backend.app.services.ai.evaluation.models import EvaluationResult, EvaluationScore, EvaluationSummary
from backend.app.services.ai.evaluation.exceptions import EvaluationNotFoundError
from backend.app.services.ai.evaluation.repository import EvaluationRepository
from backend.app.services.ai.reports.exceptions import ReportError, ReportGenerationError, InvalidReportError
from backend.app.services.ai.reports.models import ReportSection, ReportResult
from backend.app.services.ai.reports.service import ReportService

@pytest.fixture
def mock_interview_repository() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_persona_service() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_evaluation_repository() -> MagicMock:
    return MagicMock()

@pytest.fixture
def report_service(
    mock_interview_repository: MagicMock,
    mock_persona_service: MagicMock,
    mock_evaluation_repository: MagicMock,
) -> ReportService:
    return ReportService(
        interview_repository=mock_interview_repository,
        persona_service=mock_persona_service,
        evaluation_repository=mock_evaluation_repository,
    )

@pytest.fixture
def sample_evaluation() -> EvaluationResult:
    return EvaluationResult(
        scores=EvaluationScore(
            overall_score=85,
            communication_score=80,
            technical_score=90,
            confidence_score=88,
        ),
        summary=EvaluationSummary(
            strengths=["Clean FastAPI code", "Understands asyncio"],
            weaknesses=["Needs better DB index knowledge"],
            recommendations=["Hire as Mid-level SWE"],
            learning_roadmap=["Read High Performance MySQL"],
        ),
        evaluated_at=datetime.now(timezone.utc),
        persona_id=PersonaType.SWE,
    )

@pytest.fixture
def sample_interview() -> InterviewSession:
    return InterviewSession(
        interview_id="interview-456",
        session_id="interview-456",
        persona_id=PersonaType.SWE,
        status=InterviewStatus.COMPLETED,
        topics=["python", "fastapi"],
        difficulty="mid",
        created_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
    )

@pytest.fixture
def sample_persona() -> Persona:
    return Persona(
        id=PersonaType.SWE,
        name="Sarah",
        role="Senior Backend Architect",
        description="Detailed-oriented interviewer",
        interview_style="analytical",
        supported_difficulty_levels=["mid", "senior"],
        focus_areas=["FastAPI", "Databases"],
        system_context="Guidelines context string",
    )

# ==========================================
# Unit Tests
# ==========================================

def test_build_executive_summary(report_service: ReportService, sample_evaluation: EvaluationResult) -> None:
    section = report_service.build_executive_summary(sample_evaluation, "Sarah")
    assert isinstance(section, ReportSection)
    assert section.title == "Executive Summary"
    # Verify strict deterministic content derived from inputs
    assert "Sarah" in section.content
    assert "85/100" in section.content
    assert "Clean FastAPI code" in section.content
    assert "Needs better DB index knowledge" in section.content
    assert "Hire as Mid-level SWE" in section.content

def test_build_performance_overview(report_service: ReportService, sample_evaluation: EvaluationResult) -> None:
    section = report_service.build_performance_overview(sample_evaluation)
    assert isinstance(section, ReportSection)
    assert section.title == "Performance Overview"
    assert "Overall Score: 85/100" in section.content
    assert "Technical Score: 90/100" in section.content
    assert "Communication Score: 80/100" in section.content
    assert "Confidence Score: 88/100" in section.content

def test_build_markdown_report(report_service: ReportService, sample_evaluation: EvaluationResult) -> None:
    exec_summary = report_service.build_executive_summary(sample_evaluation, "Sarah")
    perf_overview = report_service.build_performance_overview(sample_evaluation)
    
    report = ReportResult(
        interview_id="interview-456",
        persona_id=PersonaType.SWE,
        executive_summary=exec_summary,
        performance_overview=perf_overview,
        strengths=sample_evaluation.summary.strengths,
        weaknesses=sample_evaluation.summary.weaknesses,
        recommendations=sample_evaluation.summary.recommendations,
        learning_roadmap=sample_evaluation.summary.learning_roadmap,
        markdown_report="Temp",
    )
    
    markdown_str = report_service.build_markdown_report(report)
    assert isinstance(markdown_str, str)
    assert "# Interview Report" in markdown_str
    assert "## Executive Summary" in markdown_str
    assert "## Performance Overview" in markdown_str
    assert "## Strengths" in markdown_str
    assert "- Clean FastAPI code" in markdown_str
    assert "## Weaknesses" in markdown_str
    assert "- Needs better DB index knowledge" in markdown_str
    assert "## Recommendations" in markdown_str
    assert "- Hire as Mid-level SWE" in markdown_str
    assert "## Learning Roadmap" in markdown_str
    assert "- Read High Performance MySQL" in markdown_str

def test_generate_report_success(
    report_service: ReportService,
    mock_interview_repository: MagicMock,
    mock_persona_service: MagicMock,
    mock_evaluation_repository: MagicMock,
    sample_interview: InterviewSession,
    sample_evaluation: EvaluationResult,
    sample_persona: Persona,
) -> None:
    interview_id = "interview-456"
    
    mock_interview_repository.get_interview.return_value = sample_interview
    mock_evaluation_repository.get_evaluation.return_value = sample_evaluation
    mock_persona_service.get_persona.return_value = sample_persona

    result = report_service.generate_report(interview_id)

    assert isinstance(result, ReportResult)
    assert result.interview_id == interview_id
    assert result.persona_id == PersonaType.SWE
    assert result.executive_summary.title == "Executive Summary"
    assert result.performance_overview.title == "Performance Overview"
    assert len(result.strengths) == 2
    assert "# Interview Report" in result.markdown_report
    
    # Assert UUID structure
    assert uuid.UUID(result.report_id).version == 4
    # Assert UTC timezone
    assert result.generated_at.tzinfo == timezone.utc

    # Verify calls
    mock_interview_repository.get_interview.assert_called_once_with(interview_id)
    mock_evaluation_repository.get_evaluation.assert_called_once_with(interview_id)
    mock_persona_service.get_persona.assert_called_once_with(PersonaType.SWE)

def test_generate_report_validation_failures(
    report_service: ReportService,
    mock_interview_repository: MagicMock,
    mock_evaluation_repository: MagicMock,
) -> None:
    # 1. Empty ID
    with pytest.raises(InvalidReportError) as exc:
        report_service.generate_report("  ")
    assert "cannot be empty" in str(exc.value)

    # 2. Missing Interview
    mock_interview_repository.get_interview.side_effect = Exception("Not Found")
    with pytest.raises(InvalidReportError) as exc:
        report_service.generate_report("missing-interview")
    assert "was not found" in str(exc.value)

    # 3. Interview Status not COMPLETED
    mock_interview_repository.get_interview.side_effect = None
    incomplete_interview = InterviewSession(
        interview_id="active-interview",
        session_id="active-interview",
        persona_id=PersonaType.SWE,
        status=InterviewStatus.IN_PROGRESS,
        topics=["python"],
        difficulty="mid",
        created_at=datetime.now(timezone.utc),
    )
    mock_interview_repository.get_interview.return_value = incomplete_interview
    with pytest.raises(InvalidReportError) as exc:
        report_service.generate_report("active-interview")
    assert "must be in 'completed' state" in str(exc.value)

    # 4. Missing Evaluation
    completed_interview = InterviewSession(
        interview_id="completed-interview",
        session_id="completed-interview",
        persona_id=PersonaType.SWE,
        status=InterviewStatus.COMPLETED,
        topics=["python"],
        difficulty="mid",
        created_at=datetime.now(timezone.utc),
    )
    mock_interview_repository.get_interview.return_value = completed_interview
    mock_evaluation_repository.get_evaluation.side_effect = EvaluationNotFoundError("Not Found")
    with pytest.raises(InvalidReportError) as exc:
        report_service.generate_report("completed-interview")
    assert "was not found" in str(exc.value)

def test_report_models_validation() -> None:
    # 1. Section validation failures
    with pytest.raises(ValueError):
        ReportSection(title="  ", content="Valid content")
    with pytest.raises(ValueError):
        ReportSection(title="Title", content="")

    # 2. Result validation failures
    with pytest.raises(ValueError):
        ReportResult(
            report_id="not-a-uuid",
            interview_id="id",
            persona_id=PersonaType.SWE,
            executive_summary=ReportSection(title="S1", content="C1"),
            performance_overview=ReportSection(title="S2", content="C2"),
            strengths=[],
            weaknesses=[],
            recommendations=[],
            learning_roadmap=[],
            markdown_report="Markdown",
        )
    with pytest.raises(ValueError):
        ReportResult(
            report_id=str(uuid.uuid4()),
            interview_id="id",
            persona_id=PersonaType.SWE,
            executive_summary=ReportSection(title="S1", content="C1"),
            performance_overview=ReportSection(title="S2", content="C2"),
            strengths=[],
            weaknesses=[],
            recommendations=[],
            learning_roadmap=[],
            markdown_report="  ",
        )

def test_serialization_and_deserialization(sample_evaluation: EvaluationResult) -> None:
    # Section serialization
    section = ReportSection(title="Section Title", content="Section content detail.")
    dump = section.model_dump()
    assert dump["title"] == "Section Title"
    assert dump["content"] == "Section content detail."

    validated = ReportSection.model_validate(dump)
    assert validated.title == section.title
    assert validated.content == section.content

    # Result serialization
    result = ReportResult(
        interview_id="interview-123",
        persona_id=PersonaType.SWE,
        executive_summary=section,
        performance_overview=section,
        strengths=["s1"],
        weaknesses=["w1"],
        recommendations=["r1"],
        learning_roadmap=["lr1"],
        markdown_report="# Markdown Report Content",
    )
    result_dump = result.model_dump()
    assert result_dump["interview_id"] == "interview-123"
    assert result_dump["persona_id"] == "swe_interviewer"
    assert result_dump["markdown_report"] == "# Markdown Report Content"
    assert "report_id" in result_dump
    assert "generated_at" in result_dump

    result_validated = ReportResult.model_validate(result_dump)
    assert result_validated.report_id == result.report_id
    assert result_validated.generated_at == result.generated_at
    assert result_validated.markdown_report == result.markdown_report

def test_determinism_under_same_inputs(
    report_service: ReportService,
    mock_interview_repository: MagicMock,
    mock_persona_service: MagicMock,
    mock_evaluation_repository: MagicMock,
    sample_interview: InterviewSession,
    sample_evaluation: EvaluationResult,
    sample_persona: Persona,
) -> None:
    interview_id = "interview-456"
    
    mock_interview_repository.get_interview.return_value = sample_interview
    mock_evaluation_repository.get_evaluation.return_value = sample_evaluation
    mock_persona_service.get_persona.return_value = sample_persona

    # Generate twice
    report1 = report_service.generate_report(interview_id)
    import time
    time.sleep(0.002)
    report2 = report_service.generate_report(interview_id)

    # Dynamic fields will differ, so we overwrite or ignore them to check strict determinism
    assert report1.report_id != report2.report_id
    assert report1.generated_at != report2.generated_at

    # Check that all deterministic summary, overview, qualitative data and markdown reports are identical
    assert report1.executive_summary == report2.executive_summary
    assert report1.performance_overview == report2.performance_overview
    assert report1.strengths == report2.strengths
    assert report1.weaknesses == report2.weaknesses
    assert report1.recommendations == report2.recommendations
    assert report1.learning_roadmap == report2.learning_roadmap
    assert report1.markdown_report == report2.markdown_report

def test_markdown_structure_headings(
    report_service: ReportService,
    mock_interview_repository: MagicMock,
    mock_persona_service: MagicMock,
    mock_evaluation_repository: MagicMock,
    sample_interview: InterviewSession,
    sample_evaluation: EvaluationResult,
    sample_persona: Persona,
) -> None:
    interview_id = "interview-456"
    mock_interview_repository.get_interview.return_value = sample_interview
    mock_evaluation_repository.get_evaluation.return_value = sample_evaluation
    mock_persona_service.get_persona.return_value = sample_persona

    report = report_service.generate_report(interview_id)
    md = report.markdown_report

    # Verify expected headings structure exists in correct markdown hierarchy
    expected_headings = [
        "# Interview Report",
        "## Executive Summary",
        "## Performance Overview",
        "## Strengths",
        "## Weaknesses",
        "## Recommendations",
        "## Learning Roadmap"
    ]
    for heading in expected_headings:
        assert heading in md
