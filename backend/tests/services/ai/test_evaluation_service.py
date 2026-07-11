# pyrefly: ignore [missing-import]
import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock, AsyncMock

from backend.app.services.ai.evaluation.exceptions import (
    EvaluationError,
    EvaluationParsingError,
    InvalidEvaluationError,
)
from backend.app.services.ai.evaluation.models import EvaluationResult, EvaluationScore, EvaluationSummary
from backend.app.services.ai.evaluation.service import EvaluationService
from backend.app.services.ai.personas.models import PersonaType, PersonaPromptContext
from backend.app.services.ai.interview.models import InterviewSession, InterviewStatus
from backend.app.services.ai.prompts.base import PromptPayload, ConversationMessage

@pytest.fixture
def mock_prompt_builder() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_gemini_service() -> MagicMock:
    mock_svc = MagicMock()
    mock_svc.generate = AsyncMock()
    return mock_svc

@pytest.fixture
def mock_conversation_service() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_persona_service() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_interview_service() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_evaluation_repository() -> MagicMock:
    return MagicMock()

@pytest.fixture
def evaluation_service(
    mock_prompt_builder: MagicMock,
    mock_gemini_service: MagicMock,
    mock_conversation_service: MagicMock,
    mock_persona_service: MagicMock,
    mock_interview_service: MagicMock,
    mock_evaluation_repository: MagicMock,
) -> EvaluationService:
    return EvaluationService(
        prompt_builder=mock_prompt_builder,
        gemini_service=mock_gemini_service,
        conversation_service=mock_conversation_service,
        persona_service=mock_persona_service,
        interview_service=mock_interview_service,
        evaluation_repository=mock_evaluation_repository,
    )

# ==========================================
# JSON Extraction & Parser Tests
# ==========================================

def test_extract_json_payload_success(evaluation_service: EvaluationService) -> None:
    # 1. Standard JSON
    raw = '{"scores": {"overall_score": 85}, "summary": {"strengths": []}}'
    assert evaluation_service._extract_json_payload(raw) == raw

    # 2. Markdown fenced JSON
    raw_markdown = '```json\n{"scores": {"overall_score": 85}, "summary": {"strengths": []}}\n```'
    assert evaluation_service._extract_json_payload(raw_markdown) == '{"scores": {"overall_score": 85}, "summary": {"strengths": []}}'

    # 3. Markdown fenced JSON without json specifier
    raw_markdown_no_spec = '```\n{"scores": {"overall_score": 85}, "summary": {"strengths": []}}\n```'
    assert evaluation_service._extract_json_payload(raw_markdown_no_spec) == '{"scores": {"overall_score": 85}, "summary": {"strengths": []}}'

    # 4. JSON with surrounding explanatory text
    raw_surrounding = 'Here is the result:\n{"scores": {"overall_score": 85}, "summary": {"strengths": []}}\nHope this helps!'
    assert evaluation_service._extract_json_payload(raw_surrounding) == '{"scores": {"overall_score": 85}, "summary": {"strengths": []}}'

    # 5. Whitespace variations
    raw_whitespace = '   \n  {  "scores"  :   {  "overall_score"  :  85  } , "summary": {"strengths": []} }  \n '
    assert evaluation_service._extract_json_payload(raw_whitespace) == '{  "scores"  :   {  "overall_score"  :  85  } , "summary": {"strengths": []} }'

def test_extract_json_payload_failures(evaluation_service: EvaluationService) -> None:
    # Empty raw response
    with pytest.raises(EvaluationParsingError) as exc:
        evaluation_service._extract_json_payload("")
    assert "empty or whitespace-only" in str(exc.value)

    # Missing braces
    with pytest.raises(EvaluationParsingError) as exc:
        evaluation_service._extract_json_payload("no braces here")
    assert "Could not find a valid JSON object structure" in str(exc.value)

    # Braces in wrong order
    with pytest.raises(EvaluationParsingError) as exc:
        evaluation_service._extract_json_payload("} opening late {")
    assert "Could not find a valid JSON object structure" in str(exc.value)

def test_parse_evaluation_response_success(evaluation_service: EvaluationService) -> None:
    # Reordered keys in JSON
    reordered_json = """
    {
      "summary": {
        "weaknesses": ["python optimization"],
        "strengths": ["async databases"],
        "learning_roadmap": ["study design patterns"],
        "recommendations": ["advance to next round"]
      },
      "scores": {
        "technical_score": 90,
        "communication_score": 85,
        "overall_score": 88,
        "confidence_score": 80
      }
    }
    """
    persona_id = PersonaType.SWE
    evaluated_at = datetime(2026, 7, 12, 12, 0, 0, tzinfo=timezone.utc)
    
    result = evaluation_service.parse_evaluation_response(reordered_json, persona_id, evaluated_at)
    
    assert isinstance(result, EvaluationResult)
    assert result.persona_id == persona_id
    assert result.evaluated_at == evaluated_at
    assert result.scores.overall_score == 88
    assert result.scores.technical_score == 90
    assert result.scores.communication_score == 85
    assert result.scores.confidence_score == 80
    assert result.summary.strengths == ["async databases"]
    assert result.summary.weaknesses == ["python optimization"]
    assert result.summary.recommendations == ["advance to next round"]
    assert result.summary.learning_roadmap == ["study design patterns"]

def test_parse_evaluation_response_validation_failures(evaluation_service: EvaluationService) -> None:
    persona_id = PersonaType.SWE

    # 1a. Malformed JSON structure (missing closing brace)
    malformed_json_braces = '{"scores": {"overall_score": 85'
    with pytest.raises(EvaluationParsingError) as exc:
        evaluation_service.parse_evaluation_response(malformed_json_braces, persona_id)
    assert "Could not find a valid JSON object structure" in str(exc.value)

    # 1b. Malformed JSON content (valid braces but invalid syntax inside)
    malformed_json_syntax = '{"scores": {"overall_score": 85,}}'
    with pytest.raises(EvaluationParsingError) as exc:
        evaluation_service.parse_evaluation_response(malformed_json_syntax, persona_id)
    assert "Failed to parse LLM response as JSON" in str(exc.value)

    # 2. Decoded JSON does not represent a JSON object (missing curly braces)
    list_json = '[1, 2, 3]'
    with pytest.raises(EvaluationParsingError) as exc:
        evaluation_service.parse_evaluation_response(list_json, persona_id)
    assert "Could not find a valid JSON object structure" in str(exc.value)

    # 3. Missing fields in schema
    missing_fields_json = '{"scores": {"overall_score": 85, "communication_score": 80, "technical_score": 90, "confidence_score": 85}}'
    with pytest.raises(InvalidEvaluationError) as exc:
        evaluation_service.parse_evaluation_response(missing_fields_json, persona_id)
    assert "Validation failed for evaluation result schema" in str(exc.value)

    # 4. Invalid scores: out of range (score > 100)
    score_out_of_range_json = """
    {
      "scores": {
        "overall_score": 105,
        "communication_score": 80,
        "technical_score": 90,
        "confidence_score": 85
      },
      "summary": {
        "strengths": ["s1"],
        "weaknesses": ["w1"],
        "recommendations": ["r1"],
        "learning_roadmap": ["l1"]
      }
    }
    """
    with pytest.raises(InvalidEvaluationError) as exc:
        evaluation_service.parse_evaluation_response(score_out_of_range_json, persona_id)
    assert "Validation failed for evaluation result schema" in str(exc.value)
    assert "105" in str(exc.value) or "less than or equal to 100" in str(exc.value)

    # 5. Invalid scores: out of range (score < 0)
    negative_score_json = """
    {
      "scores": {
        "overall_score": 85,
        "communication_score": -10,
        "technical_score": 90,
        "confidence_score": 85
      },
      "summary": {
        "strengths": ["s1"],
        "weaknesses": ["w1"],
        "recommendations": ["r1"],
        "learning_roadmap": ["l1"]
      }
    }
    """
    with pytest.raises(InvalidEvaluationError) as exc:
        evaluation_service.parse_evaluation_response(negative_score_json, persona_id)
    assert "Validation failed for evaluation result schema" in str(exc.value)
    assert "-10" in str(exc.value) or "greater than or equal to 0" in str(exc.value)


# ==========================================
# evaluate_interview Orchestration Tests
# ==========================================

@pytest.mark.anyio
async def test_evaluate_interview_success(
    evaluation_service: EvaluationService,
    mock_interview_service: MagicMock,
    mock_conversation_service: MagicMock,
    mock_persona_service: MagicMock,
    mock_prompt_builder: MagicMock,
    mock_gemini_service: MagicMock,
) -> None:
    interview_id = "test-interview-123"
    persona_id = PersonaType.SWE

    # Mock InterviewSession
    mock_session = InterviewSession(
        interview_id=interview_id,
        session_id=interview_id,
        persona_id=persona_id,
        status=InterviewStatus.COMPLETED,
        topics=["python", "django"],
        difficulty="mid",
        created_at=datetime.now(timezone.utc),
    )
    mock_interview_service.repository.get_interview.return_value = mock_session

    # Mock Conversation History
    mock_history = [
        ConversationMessage(role="interviewer", content="Explain decorator pattern."),
        ConversationMessage(role="candidate", content="It wraps a function to change its behavior."),
    ]
    mock_conversation_service.build_llm_ready_history.return_value = mock_history

    # Mock Persona context
    mock_persona_context = PersonaPromptContext(
        persona_name="SWE Persona",
        persona_context="SWE Guidelines"
    )
    mock_persona_service.get_prompt_context.return_value = mock_persona_context

    # Mock PromptBuilder
    mock_payload = PromptPayload(system_prompt="system evaluation prompt", user_prompt="user prompt")
    mock_prompt_builder.build_interview_evaluation_prompt.return_value = mock_payload

    # Mock GeminiService response
    mock_gemini_response = """
    {
      "scores": {
        "overall_score": 90,
        "communication_score": 85,
        "technical_score": 92,
        "confidence_score": 88
      },
      "summary": {
        "strengths": ["Clear explanation of patterns"],
        "weaknesses": ["Missed real-world FastAPI comparison"],
        "recommendations": ["Hire"],
        "learning_roadmap": ["Study async hooks"]
      }
    }
    """
    mock_gemini_service.generate.return_value = mock_gemini_response

    # Execute
    result = await evaluation_service.evaluate_interview(interview_id)

    # Verify
    assert isinstance(result, EvaluationResult)
    assert result.persona_id == persona_id
    assert result.scores.overall_score == 90
    assert result.summary.strengths == ["Clear explanation of patterns"]
    
    # Verify interactions
    mock_interview_service.repository.get_interview.assert_called_once_with(interview_id)
    mock_conversation_service.build_llm_ready_history.assert_called_once_with(interview_id)
    mock_persona_service.get_prompt_context.assert_called_once_with(persona_id)
    mock_prompt_builder.build_interview_evaluation_prompt.assert_called_once_with(
        persona_context="SWE Guidelines",
        history=mock_history
    )
    mock_gemini_service.generate.assert_called_once_with(
        system_prompt="system evaluation prompt",
        user_prompt="user prompt",
        temperature=0.0
    )
    evaluation_service.evaluation_repository.save_evaluation.assert_called_once_with(interview_id, result)

@pytest.mark.anyio
async def test_evaluate_interview_session_not_found(
    evaluation_service: EvaluationService,
    mock_interview_service: MagicMock,
) -> None:
    interview_id = "missing-id"
    mock_interview_service.repository.get_interview.side_effect = Exception("Not found")

    with pytest.raises(InvalidEvaluationError) as exc:
        await evaluation_service.evaluate_interview(interview_id)
    assert "was not found" in str(exc.value)

@pytest.mark.anyio
async def test_evaluate_interview_status_not_completed(
    evaluation_service: EvaluationService,
    mock_interview_service: MagicMock,
) -> None:
    interview_id = "active-id"
    mock_session = InterviewSession(
        interview_id=interview_id,
        session_id=interview_id,
        persona_id=PersonaType.SWE,
        status=InterviewStatus.IN_PROGRESS,
        topics=["python"],
        difficulty="mid",
        created_at=datetime.now(timezone.utc),
    )
    mock_interview_service.repository.get_interview.return_value = mock_session

    with pytest.raises(InvalidEvaluationError) as exc:
        await evaluation_service.evaluate_interview(interview_id)
    assert "Status must be 'completed'" in str(exc.value)

@pytest.mark.anyio
async def test_evaluate_interview_empty_history(
    evaluation_service: EvaluationService,
    mock_interview_service: MagicMock,
    mock_conversation_service: MagicMock,
) -> None:
    interview_id = "empty-history-id"
    mock_session = InterviewSession(
        interview_id=interview_id,
        session_id=interview_id,
        persona_id=PersonaType.SWE,
        status=InterviewStatus.COMPLETED,
        topics=["python"],
        difficulty="mid",
        created_at=datetime.now(timezone.utc),
    )
    mock_interview_service.repository.get_interview.return_value = mock_session
    mock_conversation_service.build_llm_ready_history.return_value = []

    with pytest.raises(InvalidEvaluationError) as exc:
        await evaluation_service.evaluate_interview(interview_id)
    assert "empty conversation history" in str(exc.value)

@pytest.mark.anyio
async def test_evaluate_interview_gemini_failure(
    evaluation_service: EvaluationService,
    mock_interview_service: MagicMock,
    mock_conversation_service: MagicMock,
    mock_persona_service: MagicMock,
    mock_prompt_builder: MagicMock,
    mock_gemini_service: MagicMock,
) -> None:
    interview_id = "gemini-fail-id"
    mock_session = InterviewSession(
        interview_id=interview_id,
        session_id=interview_id,
        persona_id=PersonaType.SWE,
        status=InterviewStatus.COMPLETED,
        topics=["python"],
        difficulty="mid",
        created_at=datetime.now(timezone.utc),
    )
    mock_interview_service.repository.get_interview.return_value = mock_session
    mock_conversation_service.build_llm_ready_history.return_value = [
        ConversationMessage(role="interviewer", content="Q")
    ]
    mock_persona_service.get_prompt_context.return_value = PersonaPromptContext(
        persona_name="P",
        persona_context="C"
    )
    mock_prompt_builder.build_interview_evaluation_prompt.return_value = PromptPayload(
        system_prompt="sys",
        user_prompt="usr"
    )
    mock_gemini_service.generate.side_effect = Exception("API error")

    with pytest.raises(EvaluationError) as exc:
        await evaluation_service.evaluate_interview(interview_id)
    assert "Gemini evaluation generation failed" in str(exc.value)
