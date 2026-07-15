import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from backend.app.main import app
from backend.app.api.dependencies import get_interview_service, get_conversation_service
from backend.app.services.ai.interview.exceptions import (
    InterviewNotFoundError,
    InterviewAlreadyCompletedError,
    InterviewError,
    InterviewGenerationError,
)
from backend.app.services.ai.personas.models import PersonaType
from backend.app.services.ai.interview.models import InterviewTurnResult

@pytest.fixture
def mock_interview_service() -> MagicMock:
    mock_svc = MagicMock()
    mock_svc.start_interview = AsyncMock()
    mock_svc.process_response = AsyncMock()
    return mock_svc

@pytest.fixture
def mock_conversation_service() -> MagicMock:
    return MagicMock()

@pytest.fixture
def client(mock_interview_service: MagicMock, mock_conversation_service: MagicMock) -> TestClient:
    app.dependency_overrides[get_interview_service] = lambda: mock_interview_service
    app.dependency_overrides[get_conversation_service] = lambda: mock_conversation_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_start_interview_success(client: TestClient, mock_interview_service: MagicMock) -> None:
    """Verifies successful start of an interview."""
    mock_interview_service.start_interview.return_value = InterviewTurnResult(
        question="What is garbage collection?",
        is_final=False,
        turn_count=1,
    )
    
    payload = {"persona_id": "swe_interviewer", "topics": ["Python"], "difficulty": "mid"}
    response = client.post("/api/v1/interviews/start", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "interview_id" in data
    assert data["question"] == "What is garbage collection?"
    assert data["question_number"] == 1
    
    mock_interview_service.start_interview.assert_called_once_with(
        interview_id=data["interview_id"],
        persona_id=PersonaType.SWE,
        topics=["Python"],
        difficulty="mid",
    )

def test_start_interview_invalid_persona(client: TestClient) -> None:
    """Verifies validation failure (422) for invalid persona enum."""
    payload = {"persona_id": "invalid_persona"}
    response = client.post("/api/v1/interviews/start", json=payload)
    assert response.status_code == 422

def test_send_message_success(
    client: TestClient,
    mock_interview_service: MagicMock,
    mock_conversation_service: MagicMock,
) -> None:
    """Verifies sending message successfully processes and returns the next question."""
    mock_interview_service.process_response.return_value = InterviewTurnResult(
        question="What are the decorators in Python?",
        is_final=False,
        turn_count=3,
    )
    mock_conversation_service.get_interviewer_turn_count.return_value = 2
    
    payload = {"message": "Garbage collection automatically manages memory."}
    response = client.post("/api/v1/interviews/session-123/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "What are the decorators in Python?"
    assert data["question_number"] == 2
    
    mock_interview_service.process_response.assert_called_once_with(
        interview_id="session-123",
        candidate_response=payload["message"],
    )
    mock_conversation_service.get_interviewer_turn_count.assert_called_once_with("session-123")

def test_send_message_empty_body(client: TestClient) -> None:
    """Verifies validation failure (422) when the message is empty or missing."""
    response = client.post("/api/v1/interviews/session-123/message", json={"message": ""})
    assert response.status_code == 422

def test_send_message_interview_not_found(client: TestClient, mock_interview_service: MagicMock) -> None:
    """Verifies 404 is returned when the interview ID does not exist."""
    mock_interview_service.process_response.side_effect = InterviewNotFoundError("Interview was not found.")
    response = client.post("/api/v1/interviews/session-123/message", json={"message": "valid answer"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Interview was not found."

def test_send_message_interview_completed_conflict(client: TestClient, mock_interview_service: MagicMock) -> None:
    """Verifies 409 is returned when sending a message to an already completed interview."""
    mock_interview_service.process_response.side_effect = InterviewAlreadyCompletedError("Interview is completed.")
    response = client.post("/api/v1/interviews/session-123/message", json={"message": "valid answer"})
    assert response.status_code == 409
    assert response.json()["detail"] == "Interview is completed."

def test_send_message_invalid_domain_request(client: TestClient, mock_interview_service: MagicMock) -> None:
    """Verifies 400 is returned when domain logic rejects the request."""
    mock_interview_service.process_response.side_effect = InterviewError("Invalid inputs.")
    response = client.post("/api/v1/interviews/session-123/message", json={"message": "valid answer"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid inputs."

def test_send_message_generation_failure(client: TestClient, mock_interview_service: MagicMock) -> None:
    """Verifies 500 is returned when LLM question generation fails."""
    mock_interview_service.process_response.side_effect = InterviewGenerationError("LLM generation failed.")
    response = client.post("/api/v1/interviews/session-123/message", json={"message": "valid answer"})
    assert response.status_code == 500
    assert response.json()["detail"] == "LLM generation failed."

def test_complete_interview_success(client: TestClient, mock_interview_service: MagicMock) -> None:
    """Verifies successful completion of an interview."""
    response = client.post("/api/v1/interviews/session-123/complete")
    assert response.status_code == 200
    assert response.json() == {"status": "completed"}
    mock_interview_service.complete_interview.assert_called_once_with("session-123")
