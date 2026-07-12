from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check() -> None:
    """Verifies that GET /health returns status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_metadata() -> None:
    """Verifies that GET / returns the correct service metadata."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "InterviewVerse AI"
    assert data["version"] == "1.0.0"
    assert data["description"] == "AI Interview Simulation Platform"

def test_openapi_generation() -> None:
    """Verifies that GET /openapi.json produces a valid OpenAPI schema."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert schema["info"]["title"] == "InterviewVerse AI"
