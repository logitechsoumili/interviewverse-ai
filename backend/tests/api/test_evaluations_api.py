import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime, timezone
from backend.app.main import app
from backend.app.api.dependencies import get_evaluation_service
from backend.app.services.ai.evaluation.exceptions import (
    EvaluationNotFoundError,
    InvalidEvaluationError,
    EvaluationParsingError,
    EvaluationError,
)
from backend.app.services.ai.personas.models import PersonaType
from backend.app.services.ai.evaluation.models import EvaluationResult, EvaluationScore, EvaluationSummary

@pytest.fixture
def mock_evaluation_service() -> MagicMock:
    mock_svc = MagicMock()
    mock_svc.evaluate_interview = AsyncMock()
    return mock_svc

@pytest.fixture
def client(mock_evaluation_service: MagicMock) -> TestClient:
    app.dependency_overrides[get_evaluation_service] = lambda: mock_evaluation_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_evaluate_interview_success(client: TestClient, mock_evaluation_service: MagicMock) -> None:
    """Verifies that POST /api/v1/interviews/{interview_id}/evaluate returns structural evaluation response."""
    now = datetime.now(timezone.utc)
    mock_evaluation_service.evaluate_interview.return_value = EvaluationResult(
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
        evaluated_at=now,
        persona_id=PersonaType.SWE,
    )
    
    response = client.post("/api/v1/interviews/session-123/evaluate")
    assert response.status_code == 200
    data = response.json()
    assert data["scores"]["overall_score"] == 85
    assert data["summary"]["strengths"] == ["Clean FastAPI code", "Understands asyncio"]
    assert data["persona_id"] == "swe_interviewer"
    
    mock_evaluation_service.evaluate_interview.assert_called_once_with("session-123")

def test_evaluate_interview_not_found(client: TestClient, mock_evaluation_service: MagicMock) -> None:
    """Verifies that 404 is returned when the evaluation/interview session is not found."""
    mock_evaluation_service.evaluate_interview.side_effect = EvaluationNotFoundError("Evaluation not found.")
    response = client.post("/api/v1/interviews/session-123/evaluate")
    assert response.status_code == 404
    assert response.json()["detail"] == "Evaluation not found."

def test_evaluate_interview_invalid_request(client: TestClient, mock_evaluation_service: MagicMock) -> None:
    """Verifies that 400 is returned for invalid request states (e.g. interview not completed)."""
    mock_evaluation_service.evaluate_interview.side_effect = InvalidEvaluationError("Interview status is not completed.")
    response = client.post("/api/v1/interviews/session-123/evaluate")
    assert response.status_code == 400
    assert response.json()["detail"] == "Interview status is not completed."

def test_evaluate_interview_parsing_failure(client: TestClient, mock_evaluation_service: MagicMock) -> None:
    """Verifies that 500 is returned when LLM response parser fails."""
    mock_evaluation_service.evaluate_interview.side_effect = EvaluationParsingError("Malformed JSON.")
    response = client.post("/api/v1/interviews/session-123/evaluate")
    assert response.status_code == 500
    assert response.json()["detail"] == "Malformed JSON."

def test_evaluate_interview_general_failure(client: TestClient, mock_evaluation_service: MagicMock) -> None:
    """Verifies that 500 is returned for other general execution failures."""
    mock_evaluation_service.evaluate_interview.side_effect = EvaluationError("Execution failure.")
    response = client.post("/api/v1/interviews/session-123/evaluate")
    assert response.status_code == 500
    assert response.json()["detail"] == "Execution failure."
