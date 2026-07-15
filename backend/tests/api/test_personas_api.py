import pytest
import uuid
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from backend.app.main import app
from backend.app.api.dependencies import get_persona_service, get_current_user
from backend.app.services.ai.personas.exceptions import PersonaNotFoundError, InvalidPersonaError
from backend.app.services.ai.personas.models import Persona, PersonaType
from app.models.user import User

mock_user_id = uuid.uuid4()
mock_user = User(id=mock_user_id, email="test@example.com", full_name="Test User")

@pytest.fixture
def mock_persona_service() -> MagicMock:
    return MagicMock()

@pytest.fixture
def client(mock_persona_service: MagicMock) -> TestClient:
    app.dependency_overrides[get_persona_service] = lambda: mock_persona_service
    app.dependency_overrides[get_current_user] = lambda: mock_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_get_personas_success(client: TestClient, mock_persona_service: MagicMock) -> None:
    """Verifies GET /api/v1/personas successfully lists summarized personas."""
    mock_persona_service.list_personas.return_value = [
        Persona(
            id=PersonaType.SWE,
            name="Alex Rivera",
            role="Senior Software Engineer Interviewer",
            description="Detailed interviewer",
            interview_style="analytical",
            supported_difficulty_levels=["junior", "mid", "senior"],
            focus_areas=["Algorithms"],
            system_context="Rules context",
        )
    ]
    response = client.get("/api/v1/personas")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "swe_interviewer",
            "name": "Alex Rivera",
            "role": "Senior Software Engineer Interviewer",
        }
    ]
    mock_persona_service.list_personas.assert_called_once_with(user_id=mock_user_id)

def test_get_persona_success(client: TestClient, mock_persona_service: MagicMock) -> None:
    """Verifies GET /api/v1/personas/{persona_id} successfully retrieves details of a persona."""
    mock_persona_service.get_persona.return_value = Persona(
        id=PersonaType.SWE,
        name="Alex Rivera",
        role="Senior Software Engineer Interviewer",
        description="Detailed interviewer",
        interview_style="analytical",
        supported_difficulty_levels=["junior", "mid", "senior"],
        focus_areas=["Algorithms"],
        system_context="Rules context",
    )
    response = client.get("/api/v1/personas/swe_interviewer")
    assert response.status_code == 200
    assert response.json() == {
        "id": "swe_interviewer",
        "name": "Alex Rivera",
        "role": "Senior Software Engineer Interviewer",
        "description": "Detailed interviewer",
        "interview_style": "analytical",
        "supported_difficulty_levels": ["junior", "mid", "senior"],
        "focus_areas": ["Algorithms"],
    }
    mock_persona_service.get_persona.assert_called_once_with("swe_interviewer", user_id=mock_user_id)

def test_get_persona_not_found(client: TestClient, mock_persona_service: MagicMock) -> None:
    """Verifies that 404 is returned when a persona is not found."""
    mock_persona_service.get_persona.side_effect = PersonaNotFoundError("Persona swe_interviewer was not found.")
    response = client.get("/api/v1/personas/swe_interviewer")
    assert response.status_code == 404
    assert response.json()["detail"] == "Persona swe_interviewer was not found."

def test_get_persona_invalid_id(client: TestClient, mock_persona_service: MagicMock) -> None:
    """Verifies that 404 is returned when an invalid or non-existent persona_id string is passed."""
    mock_persona_service.get_persona.side_effect = PersonaNotFoundError("Persona invalid_persona was not found.")
    response = client.get("/api/v1/personas/invalid_persona")
    assert response.status_code == 404

def test_get_persona_domain_validation_error(client: TestClient, mock_persona_service: MagicMock) -> None:
    """Verifies that 400 is returned when a domain validation exception is raised."""
    mock_persona_service.get_persona.side_effect = InvalidPersonaError("Persona definition is invalid.")
    response = client.get("/api/v1/personas/swe_interviewer")
    assert response.status_code == 400
    assert response.json()["detail"] == "Persona definition is invalid."
