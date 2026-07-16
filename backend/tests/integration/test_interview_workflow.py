import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock

from backend.app.main import app
from backend.app.api.dependencies import get_gemini_service
from backend.app.services.ai.gemini.service import GeminiService
from backend.app.services.ai.personas.models import PersonaType
from backend.app.services.ai.interview.models import InterviewStatus

# Import repositories directly to verify state consistency
from backend.app.services.ai.interview.dependencies import get_interview_repository
from backend.app.services.ai.conversation.dependencies import get_conversation_repository

@pytest.fixture
def mock_gemini_client() -> MagicMock:
    """Fixture providing a mock client conforming to GeminiClientProtocol."""
    client = MagicMock()
    client.generate_content = AsyncMock()
    return client

@pytest.fixture
def client(mock_gemini_client: MagicMock) -> TestClient:
    """Provides a TestClient with GeminiService using the mock client."""
    from backend.app.core.config import get_settings
    settings = get_settings()
    
    # Real GeminiService initialized with mock client
    real_gemini_service = GeminiService(
        client=mock_gemini_client,
        model=settings.GEMINI_MODEL,
        temperature=settings.GEMINI_TEMPERATURE,
    )
    
    app.dependency_overrides[get_gemini_service] = lambda: real_gemini_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def interview_repo(db_session):
    return get_interview_repository(db=db_session)

@pytest.fixture
def conversation_repo(db_session):
    return get_conversation_repository(db=db_session)


# ==========================================
# Workflow Integration Tests
# ==========================================

@pytest.mark.anyio
async def test_full_interview_lifecycle(
    client: TestClient,
    mock_gemini_client: MagicMock,
    interview_repo,
    conversation_repo,
) -> None:
    """Verifies complete interview flow from persona selection to completion, checking both API and repos."""
    
    # 1. Persona Selection
    response = client.get("/api/v1/personas")
    assert response.status_code == 200
    personas = response.json()
    assert len(personas) > 0
    assert any(p["id"] == "swe_interviewer" for p in personas)

    # 2. Start Interview
    mock_gemini_client.generate_content.return_value = "What is polymorphism?"
    
    payload = {
        "persona_id": "swe_interviewer",
        "topics": ["Python", "OOP"],
        "difficulty": "mid"
    }
    response = client.post("/api/v1/interviews/start", json=payload)
    assert response.status_code == 200
    data = response.json()
    interview_id = data["interview_id"]
    assert data["question"] == "What is polymorphism?"
    assert data["question_number"] == 1

    # Verify repository state: Interview session is created and active
    interview_session = interview_repo.get_interview(interview_id)
    assert interview_session.interview_id == interview_id
    assert interview_session.status == InterviewStatus.IN_PROGRESS
    assert interview_session.persona_id == PersonaType.SWE

    # Verify repository state: Conversation session is active with 1 turn (question 1)
    conv_session = conversation_repo.get_session(interview_id)
    assert conv_session.is_active is True
    assert len(conv_session.turns) == 1
    assert conv_session.turns[0].content == "What is polymorphism?"

    # 3. Exchange Messaging turns
    mock_gemini_client.generate_content.return_value = "Excellent. Explain encapsulation."
    
    msg_payload = {"message": "Polymorphism means having many forms."}
    msg_response = client.post(f"/api/v1/interviews/{interview_id}/message", json=msg_payload)
    assert msg_response.status_code == 200
    msg_data = msg_response.json()
    assert msg_data["question"] == "Excellent. Explain encapsulation."
    assert msg_data["question_number"] == 2

    # Verify repository state after turn exchange
    conv_session = conversation_repo.get_session(interview_id)
    assert len(conv_session.turns) == 3  # Q1, A1, Q2
    assert conv_session.turns[1].content == msg_payload["message"]
    assert conv_session.turns[2].content == "Excellent. Explain encapsulation."

    # 4. Complete Interview
    complete_response = client.post(f"/api/v1/interviews/{interview_id}/complete")
    assert complete_response.status_code == 200
    assert complete_response.json() == {"status": "completed"}

    # Verify repository state: Interview is COMPLETED and Conversation is deactivated
    interview_session = interview_repo.get_interview(interview_id)
    assert interview_session.status == InterviewStatus.COMPLETED
    
    conv_session = conversation_repo.get_session(interview_id)
    assert conv_session.is_active is False


# ==========================================
# Failure Scenarios
# ==========================================

def test_start_interview_nonexistent_persona_failure(client: TestClient) -> None:
    """Verifies that starting with a nonexistent persona yields 404 not found."""
    response = client.post("/api/v1/interviews/start", json={"persona_id": "invalid"})
    assert response.status_code == 404

@pytest.mark.anyio
async def test_start_interview_custom_persona_success(
    client: TestClient,
    mock_gemini_client: MagicMock,
) -> None:
    """Verifies successful start of an interview using a custom persona created by the user."""
    # 1. Create a custom persona first
    custom_persona_payload = {
        "id": "my_custom_qa_interviewer",
        "name": "Custom QA Interviewer",
        "role": "QA Lead",
        "description": "Evaluates testing capability.",
        "interview_style": "rigorous",
        "supported_difficulty_levels": ["mid", "senior"],
        "focus_areas": ["Automation", "Security"],
        "system_context": "You are a custom QA lead."
    }
    create_resp = client.post("/api/v1/personas", json=custom_persona_payload)
    assert create_resp.status_code == 201

    # 2. Start interview with the custom persona
    mock_gemini_client.generate_content.return_value = "What is Selenium?"
    payload = {
        "persona_id": "my_custom_qa_interviewer",
        "topics": ["Testing", "Selenium"],
        "difficulty": "mid"
    }
    response = client.post("/api/v1/interviews/start", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "interview_id" in data
    assert data["question"] == "What is Selenium?"
    assert data["question_number"] == 1

def test_send_message_missing_session(client: TestClient) -> None:
    """Verifies that sending a message to a nonexistent interview returns 404."""
    response = client.post("/api/v1/interviews/missing-id/message", json={"message": "hello"})
    assert response.status_code == 404

@pytest.mark.anyio
async def test_send_message_completed_conflict(
    client: TestClient,
    mock_gemini_client: MagicMock,
) -> None:
    """Verifies that sending a message to an already completed interview returns 409 conflict."""
    # Start and complete interview
    mock_gemini_client.generate_content.return_value = "Question"
    start_resp = client.post("/api/v1/interviews/start", json={"persona_id": "swe_interviewer"})
    interview_id = start_resp.json()["interview_id"]
    
    client.post(f"/api/v1/interviews/{interview_id}/complete")
    
    # Try messaging completed session
    msg_resp = client.post(f"/api/v1/interviews/{interview_id}/message", json={"message": "hello"})
    assert msg_resp.status_code == 409

def test_send_empty_message(client: TestClient) -> None:
    """Verifies that sending an empty answer triggers a validation failure (422)."""
    response = client.post("/api/v1/interviews/some-id/message", json={"message": ""})
    assert response.status_code == 422
