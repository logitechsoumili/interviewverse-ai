import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock, AsyncMock

from backend.app.services.ai.personas.models import PersonaType, Persona, PersonaPromptContext
from backend.app.services.ai.personas.service import PersonaService
from backend.app.services.ai.conversation.models import ConversationSession, SpeakerType, ConversationTurn
from backend.app.services.ai.conversation.repository import ConversationRepository
from backend.app.services.ai.conversation.service import ConversationService
from backend.app.services.ai.prompts.builders import PromptBuilder
from backend.app.services.ai.prompts.base import PromptPayload, ConversationMessage
from backend.app.services.ai.gemini.service import GeminiService
from backend.app.services.ai.interview.models import InterviewSession, InterviewTurnResult, InterviewStatus
from backend.app.services.ai.interview.repository import InterviewRepository
from backend.app.services.ai.interview.service import InterviewService
from backend.app.services.ai.interview.exceptions import (
    InterviewError,
    InterviewNotFoundError,
    InterviewAlreadyCompletedError,
    InterviewGenerationError,
)

# ==========================================
# Fixtures
# ==========================================

@pytest.fixture
def persona_service() -> PersonaService:
    service = MagicMock(spec=PersonaService)
    # Default mocks
    persona = Persona.model_construct(
        id=PersonaType.SWE,
        name="Alex Rivera",
        role="Senior Software Engineer Interviewer",
        description="Desc",
        interview_style="analytical",
        supported_difficulty_levels=["mid"],
        focus_areas=["Coding"],
        system_context="Sys"
    )
    service.get_persona.return_value = persona
    service.get_prompt_context.return_value = PersonaPromptContext(
        persona_name="Alex Rivera",
        persona_context="Role: SWE. Focus Areas: Coding."
    )
    return service

@pytest.fixture
def conversation_repo() -> ConversationRepository:
    return ConversationRepository()

@pytest.fixture
def conversation_service(conversation_repo: ConversationRepository) -> ConversationService:
    return ConversationService(repository=conversation_repo)

@pytest.fixture
def prompt_builder() -> PromptBuilder:
    builder = MagicMock(spec=PromptBuilder)
    builder.build_interview_prompt.return_value = PromptPayload(
        system_prompt="System instructions",
        user_prompt="User instructions"
    )
    return builder

@pytest.fixture
def gemini_service() -> GeminiService:
    service = MagicMock(spec=GeminiService)
    service.generate = AsyncMock(return_value="Mocked LLM Question?")
    return service

@pytest.fixture
def interview_repo() -> InterviewRepository:
    return InterviewRepository()

@pytest.fixture
def interview_service(
    persona_service: PersonaService,
    conversation_service: ConversationService,
    prompt_builder: PromptBuilder,
    gemini_service: GeminiService,
    interview_repo: InterviewRepository,
) -> InterviewService:
    return InterviewService(
        persona_service=persona_service,
        conversation_service=conversation_service,
        prompt_builder=prompt_builder,
        gemini_service=gemini_service,
        repository=interview_repo
    )


# ==========================================
# Repository Tests
# ==========================================

def test_repo_operations(interview_repo: InterviewRepository) -> None:
    """Verifies that create, get, update, complete, and delete operate correctly on repository."""
    session = InterviewSession(
        interview_id="int_1",
        session_id="int_1",
        persona_id=PersonaType.HR,
        status=InterviewStatus.STARTING,
        topics=["Culture"],
        difficulty="mid"
    )
    
    # 1. Create
    created = interview_repo.create_interview(session)
    assert created.interview_id == "int_1"

    # Duplicate create raises error
    with pytest.raises(InterviewError):
        interview_repo.create_interview(session)

    # 2. Get
    retrieved = interview_repo.get_interview("int_1")
    assert retrieved.interview_id == "int_1"
    
    # Get missing raises error
    with pytest.raises(InterviewNotFoundError):
        interview_repo.get_interview("missing_id")

    # 3. Update
    retrieved.status = InterviewStatus.IN_PROGRESS
    updated = interview_repo.update_interview(retrieved)
    assert updated.status == InterviewStatus.IN_PROGRESS

    # 4. Complete
    completed = interview_repo.complete_interview("int_1")
    assert completed.status == InterviewStatus.COMPLETED
    assert completed.completed_at is not None

    # 5. Delete
    interview_repo.delete_interview("int_1")
    with pytest.raises(InterviewNotFoundError):
        interview_repo.get_interview("int_1")


# ==========================================
# Service Orchestration Tests
# ==========================================

@pytest.mark.anyio
async def test_start_interview_success(interview_service: InterviewService, interview_repo: InterviewRepository) -> None:
    """Verifies starting an interview validates dependencies, seeds history, and stores question."""
    res = await interview_service.start_interview(
        interview_id="int_123",
        persona_id=PersonaType.SWE,
        topics=["Data Structures"],
        difficulty="senior"
    )
    
    # Verify InterviewTurnResult
    assert isinstance(res, InterviewTurnResult)
    assert res.question == "Mocked LLM Question?"
    assert res.is_final is False
    assert res.turn_count == 1  # 1 interviewer turn

    # Verify conversation session was created and contains the turn
    turns = interview_service.conversation_service.retrieve_conversation_history("int_123")
    assert len(turns) == 1
    assert turns[0].role == SpeakerType.INTERVIEWER
    assert turns[0].content == "Mocked LLM Question?"

    # Verify interview session was stored
    session = interview_repo.get_interview("int_123")
    assert session.status == InterviewStatus.IN_PROGRESS
    assert session.difficulty == "senior"

@pytest.mark.anyio
async def test_process_response_success(interview_service: InterviewService, gemini_service: MagicMock) -> None:
    """Verifies response processing stores responses, renders builders, and returns follow-ups."""
    # Return different questions for opening and follow-up to bypass duplicate checks
    gemini_service.generate.side_effect = ["Mocked LLM Question?", "Follow-up question?"]

    # Start interview first to setup session state
    await interview_service.start_interview(
        interview_id="int_123",
        persona_id=PersonaType.SWE,
        topics=["Data Structures"],
        difficulty="senior"
    )

    # Process response
    res = await interview_service.process_response(
        interview_id="int_123",
        candidate_response="I like arrays."
    )

    assert isinstance(res, InterviewTurnResult)
    assert res.question == "Follow-up question?"
    assert res.is_final is False
    assert res.turn_count == 3  # 1 opening + 1 candidate + 1 follow-up = 3 total turns

    # Verify turns list
    turns = interview_service.conversation_service.retrieve_conversation_history("int_123")
    assert len(turns) == 3
    assert turns[1].role == SpeakerType.CANDIDATE
    assert turns[1].content == "I like arrays."
    assert turns[2].role == SpeakerType.INTERVIEWER
    assert turns[2].content == "Follow-up question?"

def test_complete_interview_success(interview_service: InterviewService, interview_repo: InterviewRepository) -> None:
    """Verifies that completing an interview updates status, deactivates conv, and marks is_final."""
    # Setup interview & conv sessions
    session = InterviewSession(
        interview_id="int_123",
        session_id="int_123",
        persona_id=PersonaType.SWE,
        status=InterviewStatus.IN_PROGRESS,
        topics=["Math"],
        difficulty="senior"
    )
    interview_repo.create_interview(session)
    interview_service.conversation_service.create_session("int_123", PersonaType.SWE)
    
    res = interview_service.complete_interview("int_123")
    
    assert res.is_final is True
    assert res.question == "The interview is completed. Thank you!"
    
    # Check repo
    updated_session = interview_repo.get_interview("int_123")
    assert updated_session.status == InterviewStatus.COMPLETED
    assert updated_session.completed_at is not None

    # Check conversation deactivation
    conv_session = interview_service.conversation_service.repository.get_session("int_123")
    assert conv_session.is_active is False


# ==========================================
# Duplicate Question Handling Tests
# ==========================================

@pytest.mark.anyio
async def test_duplicate_question_retry_success(interview_service: InterviewService, gemini_service: MagicMock) -> None:
    """Verifies that if a duplicate question is generated, it retries and succeeds if uniqueness is hit."""
    # Start interview
    await interview_service.start_interview(
        interview_id="int_123",
        persona_id=PersonaType.SWE,
        topics=["Recursion"],
        difficulty="mid"
    )

    # Mock has_similar_question to return True once (duplicate), then False (unique)
    original_has_similar = interview_service.conversation_service.has_similar_question
    mock_has_similar = MagicMock()
    mock_has_similar.side_effect = [True, False]
    interview_service.conversation_service.has_similar_question = mock_has_similar

    # Gemini generate returns two different questions
    gemini_service.generate.side_effect = ["Duplicate Question?", "Unique Question?"]

    res = await interview_service.process_response("int_123", "Answer")
    assert res.question == "Unique Question?"
    assert mock_has_similar.call_count == 2

@pytest.mark.anyio
async def test_duplicate_question_max_retries_failure(interview_service: InterviewService, gemini_service: MagicMock) -> None:
    """Verifies that if uniqueness cannot be achieved after max retries, raises InterviewGenerationError."""
    await interview_service.start_interview(
        interview_id="int_123",
        persona_id=PersonaType.SWE,
        topics=["Recursion"],
        difficulty="mid"
    )

    # has_similar_question always returns True (always duplicate)
    mock_has_similar = MagicMock(return_value=True)
    interview_service.conversation_service.has_similar_question = mock_has_similar

    with pytest.raises(InterviewGenerationError) as exc_info:
        await interview_service.process_response("int_123", "Answer")
        
    assert "Failed to generate a unique question" in str(exc_info.value)
    # Total calls: 1 initial + 3 retries = 4
    assert mock_has_similar.call_count == 4


# ==========================================
# Validation Failures Tests
# ==========================================

@pytest.mark.anyio
async def test_validation_failures(interview_service: InterviewService, interview_repo: InterviewRepository) -> None:
    """Verifies validations reject empty inputs, invalid personas, and completed interviews."""
    # Empty ID start
    with pytest.raises(InterviewError):
        await interview_service.start_interview("", PersonaType.HR, ["Culture"], "mid")

    # Empty topics start
    with pytest.raises(InterviewError):
        await interview_service.start_interview("id", PersonaType.HR, [], "mid")

    # Completed interview response processing
    session = InterviewSession(
        interview_id="completed_int",
        session_id="completed_int",
        persona_id=PersonaType.SWE,
        status=InterviewStatus.COMPLETED,
        topics=["Math"],
        difficulty="mid"
    )
    interview_repo.create_interview(session)
    
    with pytest.raises(InterviewAlreadyCompletedError):
        await interview_service.process_response("completed_int", "Response")

    with pytest.raises(InterviewAlreadyCompletedError):
        interview_service.complete_interview("completed_int")
