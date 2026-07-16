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
def interview_repo(db_session):
    return get_interview_repository(db=db_session)

@pytest.fixture
def evaluation_repo(db_session):
    return get_evaluation_repository(db=db_session)


# ==========================================
# Evaluation Integration Tests
# ==========================================

@pytest.mark.anyio
async def test_evaluation_flow_success(
    client: TestClient,
    mock_gemini_client: MagicMock,
    interview_repo,
    evaluation_repo,
) -> None:
    """Verifies complete evaluation generation, verifying repository persistence and structure."""
    
    # 1. Start and complete interview
    mock_gemini_client.generate_content.return_value = "Question?"
    start_resp = client.post("/api/v1/interviews/start", json={"persona_id": "swe_interviewer"})
    interview_id = start_resp.json()["interview_id"]
    
    # Send a candidate message
    client.post(f"/api/v1/interviews/{interview_id}/message", json={"message": "Candidate response."})
    
    # Complete interview
    client.post(f"/api/v1/interviews/{interview_id}/complete")
    
    # Mock Gemini evaluation JSON payload
    mock_gemini_client.generate_content.return_value = """
    {
      "scores": {
        "overall_score": 85,
        "communication_score": 80,
        "technical_score": 90,
        "confidence_score": 85
      },
      "summary": {
        "strengths": ["Clear communication"],
        "weaknesses": ["None"],
        "recommendations": ["Advance"],
        "learning_roadmap": ["Advanced study"]
      }
    }
    """
    
    # 2. Evaluate
    response = client.post(f"/api/v1/interviews/{interview_id}/evaluate")
    assert response.status_code == 200
    data = response.json()
    assert data["scores"]["overall_score"] == 85
    assert data["summary"]["strengths"] == ["Clear communication"]
    assert data["persona_id"] == "swe_interviewer"

    # 3. Verify EvaluationRepository state persistence directly
    stored_eval = evaluation_repo.get_evaluation(interview_id)
    assert stored_eval.scores.overall_score == 85
    assert stored_eval.summary.strengths == ["Clear communication"]
    assert stored_eval.persona_id == PersonaType.SWE


# ==========================================
# Evaluation Failure Scenarios
# ==========================================

def test_evaluate_missing_session(client: TestClient) -> None:
    """Verifies that evaluating a nonexistent session returns 400."""
    response = client.post("/api/v1/interviews/nonexistent-id/evaluate")
    assert response.status_code == 400
    assert "was not found" in response.json()["detail"].lower()

@pytest.mark.anyio
async def test_evaluate_in_progress_session(
    client: TestClient,
    mock_gemini_client: MagicMock,
) -> None:
    """Verifies that evaluating an in-progress session returns 400 bad request."""
    # Start but do not complete
    mock_gemini_client.generate_content.return_value = "Question?"
    start_resp = client.post("/api/v1/interviews/start", json={"persona_id": "swe_interviewer"})
    interview_id = start_resp.json()["interview_id"]
    
    response = client.post(f"/api/v1/interviews/{interview_id}/evaluate")
    assert response.status_code == 400
    assert "must be" in response.json()["detail"].lower()
