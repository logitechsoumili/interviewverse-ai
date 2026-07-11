import pytest
import json
from datetime import datetime, timezone
from backend.app.services.ai.personas.models import PersonaType
from backend.app.services.ai.prompts.base import ConversationMessage
from backend.app.services.ai.conversation.models import ConversationSession, ConversationTurn, SpeakerType
from backend.app.services.ai.conversation.repository import ConversationRepository
from backend.app.services.ai.conversation.service import ConversationService
from backend.app.services.ai.conversation.exceptions import (
    ConversationNotFoundError,
    InvalidConversationError,
)

@pytest.fixture
def repository() -> ConversationRepository:
    """Fixture providing a clean ConversationRepository."""
    return ConversationRepository()

@pytest.fixture
def service(repository: ConversationRepository) -> ConversationService:
    """Fixture providing a ConversationService."""
    return ConversationService(repository=repository)


# ==========================================
# Repository & Session Control Tests
# ==========================================

def test_create_session_success(service: ConversationService) -> None:
    """Verifies that create_session creates the session with correct metadata and is active."""
    session = service.create_session(session_id="session_123", persona_id=PersonaType.HR)
    assert isinstance(session, ConversationSession)
    assert session.session_id == "session_123"
    assert session.persona_id == PersonaType.HR
    assert session.is_active is True
    assert len(session.turns) == 0

def test_create_session_duplicate_raises_error(service: ConversationService) -> None:
    """Verifies that creating a session with a duplicate ID raises InvalidConversationError."""
    service.create_session("session_123", PersonaType.HR)
    with pytest.raises(InvalidConversationError) as exc_info:
        service.create_session("session_123", PersonaType.SWE)
    assert "already exists" in str(exc_info.value)

def test_get_session_success(service: ConversationService) -> None:
    """Verifies successful retrieval of a session."""
    service.create_session("session_123", PersonaType.HR)
    session = service.repository.get_session("session_123")
    assert session.session_id == "session_123"

def test_get_session_missing_raises_error(service: ConversationService) -> None:
    """Verifies lookup of missing session ID raises ConversationNotFoundError."""
    with pytest.raises(ConversationNotFoundError) as exc_info:
        service.retrieve_conversation_history("missing_session")
    assert "was not found" in str(exc_info.value)

def test_delete_session_success(service: ConversationService) -> None:
    """Verifies that delete_session removes the session, and subsequent lookups fail."""
    service.create_session("session_123", PersonaType.HR)
    # Check exists
    assert isinstance(service.repository.get_session("session_123"), ConversationSession)
    
    # Delete
    service.repository.delete_session("session_123")
    
    # Check missing
    with pytest.raises(ConversationNotFoundError):
        service.repository.get_session("session_123")

def test_delete_session_missing_raises_error(service: ConversationService) -> None:
    """Verifies deleting a non-existent session ID raises ConversationNotFoundError."""
    with pytest.raises(ConversationNotFoundError) as exc_info:
        service.repository.delete_session("non_existent")
    assert "was not found" in str(exc_info.value)


# ==========================================
# Conversation Turns & Counts Tests
# ==========================================

def test_append_turns_and_counts(service: ConversationService) -> None:
    """Verifies appending turns and getting total, interviewer, and candidate counts."""
    service.create_session("session_123", PersonaType.SWE)
    
    # Verify initial counts
    assert service.get_turn_count("session_123") == 0
    assert service.get_interviewer_turn_count("session_123") == 0
    assert service.get_candidate_turn_count("session_123") == 0

    # Add interviewer turn
    service.append_interviewer_turn("session_123", "What is inheritance?")
    assert service.get_turn_count("session_123") == 1
    assert service.get_interviewer_turn_count("session_123") == 1
    assert service.get_candidate_turn_count("session_123") == 0

    # Add candidate turn
    service.append_candidate_turn("session_123", "Inheritance allows a subclass to inherit attributes.")
    assert service.get_turn_count("session_123") == 2
    assert service.get_interviewer_turn_count("session_123") == 1
    assert service.get_candidate_turn_count("session_123") == 1

    # Verify history structures
    history = service.retrieve_conversation_history("session_123")
    assert len(history) == 2
    assert history[0].role == SpeakerType.INTERVIEWER
    assert history[0].content == "What is inheritance?"
    assert history[1].role == SpeakerType.CANDIDATE
    assert history[1].content == "Inheritance allows a subclass to inherit attributes."


# ==========================================
# LLM-Ready History Conversion Tests
# ==========================================

def test_build_llm_ready_history(service: ConversationService) -> None:
    """Verifies that build_llm_ready_history converts turns to ConversationMessage list."""
    service.create_session("session_123", PersonaType.MLE)
    service.append_interviewer_turn("session_123", "Explain gradient descent.")
    service.append_candidate_turn("session_123", "It optimizes weights iteratively.")
    
    llm_history = service.build_llm_ready_history("session_123")
    
    assert isinstance(llm_history, list)
    assert len(llm_history) == 2
    assert all(isinstance(msg, ConversationMessage) for msg in llm_history)
    
    assert llm_history[0].role == "interviewer"
    assert llm_history[0].content == "Explain gradient descent."
    assert llm_history[1].role == "candidate"
    assert llm_history[1].content == "It optimizes weights iteratively."


# ==========================================
# Validation Failures Tests
# ==========================================

def test_service_validation_failures(service: ConversationService) -> None:
    """Verifies validations reject empty session IDs, empty messages, or missing sessions."""
    # Empty session ID
    with pytest.raises(InvalidConversationError) as exc_info:
        service.create_session("   ", PersonaType.HR)
    assert "Session ID cannot be empty" in str(exc_info.value)

    # Invalid persona type
    with pytest.raises(InvalidConversationError) as exc_info:
        service.create_session("session_123", "invalid_persona")  # type: ignore
    assert "persona_id must be a valid PersonaType" in str(exc_info.value)

    service.create_session("session_123", PersonaType.HR)

    # Empty interviewer turn content
    with pytest.raises(InvalidConversationError) as exc_info:
        service.append_interviewer_turn("session_123", "")
    assert "Message content cannot be empty" in str(exc_info.value)

    # Empty candidate turn content
    with pytest.raises(InvalidConversationError) as exc_info:
        service.append_candidate_turn("session_123", "  ")
    assert "Message content cannot be empty" in str(exc_info.value)

    # Appending to missing session ID
    with pytest.raises(ConversationNotFoundError) as exc_info:
        service.append_interviewer_turn("missing_session_id", "Hello")
    assert "was not found" in str(exc_info.value)


# ==========================================
# Similarity / Duplicate Detection Tests
# ==========================================

def test_has_similar_question(service: ConversationService) -> None:
    """Verifies that similar question checking works for exact, close, and unique inputs."""
    service.create_session("session_123", PersonaType.SWE)
    
    # Empty history check
    assert service.has_similar_question("session_123", "What is polymorphism?") is False

    # Add questions
    service.append_interviewer_turn("session_123", "Explain the concept of polymorphism.")
    service.append_candidate_turn("session_123", "Polymorphism means many forms.")
    service.append_interviewer_turn("session_123", "Describe system design principles.")

    # 1. Exact match (case insensitive, stripped)
    assert service.has_similar_question("session_123", "  EXPLAIN THE CONCEPT OF POLYMORPHISM.  ") is True

    # 2. Highly similar match (ratio above default 0.8)
    assert service.has_similar_question("session_123", "Can you explain the concept of polymorphism?") is True

    # 3. Unique question
    assert service.has_similar_question("session_123", "What is garbage collection?") is False

    # 4. Threshold override checks
    # "Explain polymorphism" vs "Explain the concept of polymorphism." has similarity ~0.76
    # It should be False at default 0.8, but True at 0.7
    assert service.has_similar_question("session_123", "Explain polymorphism", similarity_threshold=0.8) is False
    assert service.has_similar_question("session_123", "Explain polymorphism", similarity_threshold=0.7) is True


# ==========================================
# Serialization Tests
# ==========================================

def test_conversation_turn_serialization() -> None:
    """Verifies that ConversationTurn Pydantic model serializes and validates correctly from JSON."""
    turn = ConversationTurn(
        role=SpeakerType.INTERVIEWER,
        content="What is virtual memory?",
        timestamp=datetime.now(timezone.utc)
    )
    serialized = turn.model_dump_json()
    
    data = json.loads(serialized)
    assert data["role"] == "interviewer"
    assert data["content"] == "What is virtual memory?"
    assert "timestamp" in data
    
    deserialized = ConversationTurn.model_validate_json(serialized)
    assert deserialized.role == turn.role
    assert deserialized.content == turn.content

def test_conversation_session_serialization() -> None:
    """Verifies that ConversationSession Pydantic model serializes and validates correctly from JSON."""
    session = ConversationSession(
        session_id="session_serialization",
        persona_id=PersonaType.SWE,
        turns=[
            ConversationTurn(role=SpeakerType.INTERVIEWER, content="Hello", timestamp=datetime.now(timezone.utc)),
            ConversationTurn(role=SpeakerType.CANDIDATE, content="Hi", timestamp=datetime.now(timezone.utc))
        ],
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    serialized = session.model_dump_json()
    
    data = json.loads(serialized)
    assert data["session_id"] == "session_serialization"
    assert data["persona_id"] == "swe_interviewer"
    assert data["is_active"] is True
    assert len(data["turns"]) == 2
    
    deserialized = ConversationSession.model_validate_json(serialized)
    assert deserialized.session_id == session.session_id
    assert deserialized.persona_id == session.persona_id
    assert deserialized.is_active == session.is_active
    assert len(deserialized.turns) == 2
