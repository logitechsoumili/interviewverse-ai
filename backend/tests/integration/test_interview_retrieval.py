import os
import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import MagicMock, AsyncMock

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models.user import User as UserORM
from app.models.persona import Persona as PersonaORM
from backend.app.services.ai.personas.models import PersonaType
from backend.app.api.dependencies import get_gemini_service
from backend.app.services.ai.gemini.service import GeminiService

DB_FILE = "test_interview_retrieval.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def mock_gemini_client() -> MagicMock:
    client = MagicMock()
    client.generate_content = AsyncMock()
    return client


@pytest.fixture(autouse=True)
def setup_db(mock_gemini_client):
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
        except PermissionError:
            pass

    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

    # Real GeminiService initialized with mock client
    from backend.app.core.config import get_settings
    settings = get_settings()
    real_gemini_service = GeminiService(
        client=mock_gemini_client,
        model=settings.GEMINI_MODEL,
        temperature=settings.GEMINI_TEMPERATURE,
    )
    app.dependency_overrides[get_gemini_service] = lambda: real_gemini_service

    # Seed the platform personas owned by a system user
    system_user_id = uuid.UUID("00000000-0000-0000-0000-000000000000")
    db = TestingSessionLocal()
    
    mock_system_user = UserORM(
        id=system_user_id,
        email="system@interviewverse.ai",
        full_name="System User",
        password_hash="disabled"
    )
    db.add(mock_system_user)
    
    default_personas = [
        PersonaORM(
            id=PersonaType.HR.value,
            user_id=system_user_id,
            name="Sarah Jenkins",
            role="HR Interviewer",
            description="A friendly, cultural-fit-focused HR representative who evaluates soft skills and core values.",
            interview_style="warm, conversational, and highly empathetic",
            supported_difficulty_levels=["junior", "mid", "senior"],
            focus_areas=["Behavioral", "Culture Fit", "Communication", "Conflict Resolution"],
            system_context=(
                "You are Sarah Jenkins, an experienced HR Interviewer. "
                "Your interview style is warm, engaging, and highly professional. "
                "You focus on evaluating behavioral competency, communication capabilities, collaboration experience, and alignment with corporate culture. "
                "Ask situational questions and look for soft skills like empathy, adaptability, and resilience."
            )
        ),
        PersonaORM(
            id=PersonaType.SWE.value,
            user_id=system_user_id,
            name="Alex Rivera",
            role="Senior Software Engineer Interviewer",
            description="A technical interviewer focused on clean code, software design principles, and problem-solving skills.",
            interview_style="analytical, technical, and highly structured",
            supported_difficulty_levels=["junior", "mid", "senior"],
            focus_areas=["Data Structures", "Algorithms", "Clean Code", "Design Patterns"],
            system_context=(
                "You are Alex Rivera, a Senior Software Engineer Interviewer. "
                "Your style is analytical, structured, and focused on technical correctness. "
                "You evaluate the candidate's software engineering fundamentals, coding efficiency, clean architecture concepts, and readability. "
                "Ask challenging technical questions and dive deep into algorithmic design choices."
            )
        )
    ]
    
    for p in default_personas:
        db.add(p)
    db.commit()
    db.close()

    yield

    app.dependency_overrides.clear()
    engine.dispose()
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
        except PermissionError:
            pass


def test_interview_retrieval_flow(mock_gemini_client: MagicMock) -> None:
    client = TestClient(app)

    # 1. Register and login User A
    user_a_payload = {
        "email": "usera_retrieval@example.com",
        "full_name": "User A",
        "password": "passwordA123"
    }
    resp = client.post("/api/v1/auth/register", json=user_a_payload)
    assert resp.status_code == 201

    login_a_payload = {
        "email": user_a_payload["email"],
        "password": user_a_payload["password"]
    }
    resp = client.post("/api/v1/auth/login", json=login_a_payload)
    assert resp.status_code == 200
    token_a = resp.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # 2. Register and login User B
    user_b_payload = {
        "email": "userb_retrieval@example.com",
        "full_name": "User B",
        "password": "passwordB123"
    }
    resp = client.post("/api/v1/auth/register", json=user_b_payload)
    assert resp.status_code == 201

    login_b_payload = {
        "email": user_b_payload["email"],
        "password": user_b_payload["password"]
    }
    resp = client.post("/api/v1/auth/login", json=login_b_payload)
    assert resp.status_code == 200
    token_b = resp.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 3. User A starts an interview
    mock_gemini_client.generate_content.return_value = "Tell me about your tech background."
    start_payload = {
        "persona_id": "swe_interviewer",
        "topics": ["Python", "Algorithms"],
        "difficulty": "mid"
    }
    resp = client.post("/api/v1/interviews/start", json=start_payload, headers=headers_a)
    assert resp.status_code == 200
    interview_data = resp.json()
    interview_id = interview_data["interview_id"]

    # 4. User A exchanges one message turn
    mock_gemini_client.generate_content.return_value = "Interesting. What are decorators?"
    msg_payload = {"message": "I have 5 years of Python experience."}
    resp = client.post(f"/api/v1/interviews/{interview_id}/message", json=msg_payload, headers=headers_a)
    assert resp.status_code == 200

    # 5. User A completes the interview
    resp = client.post(f"/api/v1/interviews/{interview_id}/complete", headers=headers_a)
    assert resp.status_code == 200

    # 6. User A evaluates the interview
    evaluation_mock_json = """
    {
        "scores": {
            "overall_score": 85,
            "communication_score": 90,
            "technical_score": 80,
            "confidence_score": 85
        },
        "summary": {
            "strengths": ["Strong verbal explanation", "Deep knowledge of decorators"],
            "weaknesses": ["Minor syntax slip on decorators examples"],
            "recommendations": ["Practice live coding"],
            "learning_roadmap": ["Advanced decorators constructs"]
        }
    }
    """
    mock_gemini_client.generate_content.return_value = evaluation_mock_json
    resp = client.post(f"/api/v1/interviews/{interview_id}/evaluate", headers=headers_a)
    assert resp.status_code == 200

    # ----------------------------------------------------
    # Verification of GET /api/v1/interviews
    # ----------------------------------------------------
    # User A lists interviews
    resp = client.get("/api/v1/interviews", headers=headers_a)
    assert resp.status_code == 200
    interviews_a = resp.json()
    assert len(interviews_a) == 1
    assert interviews_a[0]["id"] == interview_id
    assert interviews_a[0]["status"] == "completed"
    assert interviews_a[0]["persona"] == "swe_interviewer"

    # User B lists interviews (should not see User A's interview)
    resp = client.get("/api/v1/interviews", headers=headers_b)
    assert resp.status_code == 200
    assert len(resp.json()) == 0

    # ----------------------------------------------------
    # Verification of GET /api/v1/interviews/{id}
    # ----------------------------------------------------
    # User A retrieves details
    resp = client.get(f"/api/v1/interviews/{interview_id}", headers=headers_a)
    assert resp.status_code == 200
    detail = resp.json()
    assert detail["status"] == "completed"
    assert detail["metadata"]["persona_id"] == "swe_interviewer"
    assert detail["metadata"]["difficulty"] == "mid"
    assert "Python" in detail["metadata"]["topics"]
    assert len(detail["conversation_summary"]) == 3
    # Verify chronological turns (interviewer opening question -> candidate response)
    assert detail["conversation_summary"][0]["role"] == "interviewer"
    assert detail["conversation_summary"][0]["content"] == "Tell me about your tech background."

    # User B retrieves User A's details -> 404
    resp = client.get(f"/api/v1/interviews/{interview_id}", headers=headers_b)
    assert resp.status_code == 404

    # Non-existent interview detail -> 404
    resp = client.get(f"/api/v1/interviews/{uuid.uuid4()}", headers=headers_a)
    assert resp.status_code == 404

    # ----------------------------------------------------
    # Verification of GET /api/v1/interviews/{id}/evaluation
    # ----------------------------------------------------
    # User A retrieves evaluation (should be direct DB query, no Gemini call)
    mock_gemini_client.generate_content.reset_mock()
    resp = client.get(f"/api/v1/interviews/{interview_id}/evaluation", headers=headers_a)
    assert resp.status_code == 200
    eval_data = resp.json()
    assert eval_data["scores"]["overall_score"] == 85
    assert "Practice live coding" in eval_data["summary"]["recommendations"]
    mock_gemini_client.generate_content.assert_not_called()  # Proves no regeneration

    # User B retrieves User A's evaluation -> 404
    resp = client.get(f"/api/v1/interviews/{interview_id}/evaluation", headers=headers_b)
    assert resp.status_code == 404

    # Fetching evaluation of non-existent session -> 404
    resp = client.get(f"/api/v1/interviews/{uuid.uuid4()}/evaluation", headers=headers_a)
    assert resp.status_code == 404

    # ----------------------------------------------------
    # Verification of unauthorized access
    # ----------------------------------------------------
    resp = client.get("/api/v1/interviews")
    assert resp.status_code == 401

    resp = client.get(f"/api/v1/interviews/{interview_id}")
    assert resp.status_code == 401

    resp = client.get(f"/api/v1/interviews/{interview_id}/evaluation")
    assert resp.status_code == 401
