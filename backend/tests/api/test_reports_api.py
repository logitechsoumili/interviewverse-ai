import pytest
import uuid
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import datetime, timezone
from backend.app.main import app
from backend.app.api.dependencies import get_report_service, get_current_user
from backend.app.services.ai.reports.exceptions import (
    ReportError,
    ReportGenerationError,
    InvalidReportError,
)
from backend.app.services.ai.personas.models import PersonaType
from backend.app.services.ai.reports.models import ReportResult, ReportSection
from app.models.user import User

mock_user_id = uuid.uuid4()
mock_user = User(id=mock_user_id, email="test@example.com", full_name="Test User")

@pytest.fixture
def mock_report_service() -> MagicMock:
    return MagicMock()

@pytest.fixture
def client(mock_report_service: MagicMock) -> TestClient:
    app.dependency_overrides[get_report_service] = lambda: mock_report_service
    app.dependency_overrides[get_current_user] = lambda: mock_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_get_report_success(client: TestClient, mock_report_service: MagicMock) -> None:
    """Verifies that GET /api/v1/interviews/{interview_id}/report returns structured report response."""
    now = datetime.now(timezone.utc)
    mock_report_service.generate_report.return_value = ReportResult(
        report_id="12345678-1234-5678-1234-567812345678",
        interview_id="session-123",
        persona_id=PersonaType.SWE,
        generated_at=now,
        executive_summary=ReportSection(title="Summary", content="Good overall."),
        performance_overview=ReportSection(title="Scores", content="Clean scores."),
        strengths=["async"],
        weaknesses=["none"],
        recommendations=["hire"],
        learning_roadmap=["none"],
        markdown_report="# Markdown Report Detail",
    )
    
    response = client.get("/api/v1/interviews/session-123/report")
    assert response.status_code == 200
    data = response.json()
    assert data["report_id"] == "12345678-1234-5678-1234-567812345678"
    assert data["executive_summary"]["title"] == "Summary"
    assert data["markdown_report"] == "# Markdown Report Detail"
    
    mock_report_service.generate_report.assert_called_once_with("session-123", user_id=mock_user_id)

def test_get_report_invalid_request(client: TestClient, mock_report_service: MagicMock) -> None:
    """Verifies that 400 is returned for invalid request states."""
    mock_report_service.generate_report.side_effect = InvalidReportError("Report parameters are invalid.")
    response = client.get("/api/v1/interviews/session-123/report")
    assert response.status_code == 400
    assert response.json()["detail"] == "Report parameters are invalid."

def test_get_report_generation_failure(client: TestClient, mock_report_service: MagicMock) -> None:
    """Verifies that 500 is returned for report generation failures."""
    mock_report_service.generate_report.side_effect = ReportGenerationError("Failed to format report.")
    response = client.get("/api/v1/interviews/session-123/report")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to format report."
