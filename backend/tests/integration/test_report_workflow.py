import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from backend.app.main import app
from backend.app.api.dependencies import get_gemini_service
from backend.app.services.ai.gemini.service import GeminiService
from backend.app.services.ai.personas.models import PersonaType
from backend.app.services.ai.interview.models import InterviewStatus

# Import repositories directly to verify state consistency and persistence
from backend.app.services.ai.interview.dependencies import get_interview_repository
from backend.app.services.ai.conversation.dependencies import get_conversation_repository
from backend.app.services.ai.evaluation.dependencies import get_evaluation_repository

@pytest.fixture
def mock_gemini_client() -> MagicMock:
    client = MagicMock()
    client.generate_content = AsyncMock()
    return client

@pytest.fixture
def client(mock_gemini_client: MagicMock) -> TestClient:
    from backend.app.core.config import get_settings
    settings = get_settings()
    
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
def interview_repo():
    return get_interview_repository()

@pytest.fixture
def conversation_repo():
    return get_conversation_repository()

@pytest.fixture
def evaluation_repo():
    return get_evaluation_repository()


# ==========================================
# Report & Journey Integration Tests
# ==========================================

@pytest.mark.anyio
async def test_complete_candidate_journey(
    client: TestClient,
    mock_gemini_client: MagicMock,
    interview_repo,
    conversation_repo,
    evaluation_repo,
) -> None:
    """Tests the complete end-to-end journey of a candidate, verifying repositories and consistency.
    
    Flow:
    1. GET persona
    2. POST start interview
    3. POST message (1)
    4. POST message (2)
    5. POST message (3)
    6. POST complete
    7. POST evaluate
    8. GET report
    """
    
    # 1. GET persona
    persona_resp = client.get("/api/v1/personas/swe_interviewer")
    assert persona_resp.status_code == 200
    assert persona_resp.json()["name"] == "Alex Rivera"

    # 2. POST start interview
    mock_gemini_client.generate_content.return_value = "What is polymorphism?"
    start_resp = client.post(
        "/api/v1/interviews/start",
        json={"persona_id": "swe_interviewer", "topics": ["Python"], "difficulty": "mid"}
    )
    assert start_resp.status_code == 200
    start_data = start_resp.json()
    interview_id = start_data["interview_id"]
    assert start_data["question_number"] == 1

    # Verify repository singleton persistence: Session state exists
    int_session = interview_repo.get_interview(interview_id)
    assert int_session.status == InterviewStatus.IN_PROGRESS
    
    conv_session = conversation_repo.get_session(interview_id)
    assert conv_session.is_active is True
    assert len(conv_session.turns) == 1

    # 3. POST message (1)
    mock_gemini_client.generate_content.return_value = "Explain encapsulation."
    m1_resp = client.post(
        f"/api/v1/interviews/{interview_id}/message",
        json={"message": "Polymorphism lets objects take many forms."}
    )
    assert m1_resp.status_code == 200
    assert m1_resp.json()["question_number"] == 2

    # Verify repository state survives across requests
    conv_session = conversation_repo.get_session(interview_id)
    assert len(conv_session.turns) == 3

    # 4. POST message (2)
    mock_gemini_client.generate_content.return_value = "What is inheritance?"
    m2_resp = client.post(
        f"/api/v1/interviews/{interview_id}/message",
        json={"message": "Encapsulation hides data internal to classes."}
    )
    assert m2_resp.status_code == 200
    assert m2_resp.json()["question_number"] == 3

    # Verify repository state survives across requests
    conv_session = conversation_repo.get_session(interview_id)
    assert len(conv_session.turns) == 5

    # 5. POST message (3)
    mock_gemini_client.generate_content.return_value = "Nice. That is all."
    m3_resp = client.post(
        f"/api/v1/interviews/{interview_id}/message",
        json={"message": "Inheritance allows subclasses to inherit properties."}
    )
    assert m3_resp.status_code == 200
    assert m3_resp.json()["question_number"] == 4

    # Verify repository state survives across requests
    conv_session = conversation_repo.get_session(interview_id)
    assert len(conv_session.turns) == 7

    # 6. POST complete
    complete_resp = client.post(f"/api/v1/interviews/{interview_id}/complete")
    assert complete_resp.status_code == 200
    assert complete_resp.json() == {"status": "completed"}

    # Verify completed state in repos
    assert interview_repo.get_interview(interview_id).status == InterviewStatus.COMPLETED
    assert conversation_repo.get_session(interview_id).is_active is False

    # 7. POST evaluate
    mock_gemini_client.generate_content.return_value = """
    {
      "scores": {
        "overall_score": 92,
        "communication_score": 88,
        "technical_score": 95,
        "confidence_score": 90
      },
      "summary": {
        "strengths": ["Excellent understanding of OOP principles"],
        "weaknesses": ["None"],
        "recommendations": ["Hire immediately"],
        "learning_roadmap": ["FastAPI Advanced concepts"]
      }
    }
    """
    eval_resp = client.post(f"/api/v1/interviews/{interview_id}/evaluate")
    assert eval_resp.status_code == 200
    eval_data = eval_resp.json()
    assert eval_data["scores"]["overall_score"] == 92

    # Verify evaluation persistence in repository
    stored_eval = evaluation_repo.get_evaluation(interview_id)
    assert stored_eval.scores.overall_score == 92
    assert stored_eval.summary.strengths == ["Excellent understanding of OOP principles"]

    # 8. GET report
    report_resp = client.get(f"/api/v1/interviews/{interview_id}/report")
    assert report_resp.status_code == 200
    report_data = report_resp.json()
    
    # Verify report consistency: Report scores match evaluation scores exactly
    assert report_data["performance_overview"]["content"] == (
        "Overall Score: 92/100\n"
        "Technical Score: 95/100\n"
        "Communication Score: 88/100\n"
        "Confidence Score: 90/100"
    )
    assert report_data["strengths"] == ["Excellent understanding of OOP principles"]
    assert report_data["weaknesses"] == ["None"]
    assert "# Interview Report" in report_data["markdown_report"]


# ==========================================
# Report Failure Scenarios
# ==========================================

def test_get_report_missing_session(client: TestClient) -> None:
    """Verifies that getting a report for a nonexistent session returns 400."""
    response = client.get("/api/v1/interviews/nonexistent-id/report")
    assert response.status_code == 400
    assert "was not found" in response.json()["detail"].lower()

@pytest.mark.anyio
async def test_get_report_in_progress_session(
    client: TestClient,
    mock_gemini_client: MagicMock,
) -> None:
    """Verifies that getting a report for an in-progress session returns 400."""
    # Start but do not complete
    mock_gemini_client.generate_content.return_value = "Question?"
    start_resp = client.post("/api/v1/interviews/start", json={"persona_id": "swe_interviewer"})
    interview_id = start_resp.json()["interview_id"]
    
    response = client.get(f"/api/v1/interviews/{interview_id}/report")
    assert response.status_code == 400

@pytest.mark.anyio
async def test_get_report_before_evaluation(
    client: TestClient,
    mock_gemini_client: MagicMock,
) -> None:
    """Verifies that getting a report before evaluation returns 400."""
    # Start and complete, but do not evaluate
    mock_gemini_client.generate_content.return_value = "Question?"
    start_resp = client.post("/api/v1/interviews/start", json={"persona_id": "swe_interviewer"})
    interview_id = start_resp.json()["interview_id"]
    
    client.post(f"/api/v1/interviews/{interview_id}/complete")
    
    response = client.get(f"/api/v1/interviews/{interview_id}/report")
    assert response.status_code == 400
    assert "was not found" in response.json()["detail"].lower()
