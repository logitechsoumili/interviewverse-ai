import os
import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models.user import User as UserORM
from app.models.persona import Persona as PersonaORM
from backend.app.services.ai.personas.models import PersonaType

DB_FILE = "test_persona_visibility.db"
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


@pytest.fixture(autouse=True)
def setup_db():
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
        except PermissionError:
            pass

    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

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
        ),
        PersonaORM(
            id=PersonaType.MLE.value,
            user_id=system_user_id,
            name="Dr. Elena Rostova",
            role="Lead Machine Learning Engineer",
            description="A specialist in machine learning, evaluating core statistical knowledge and model productionization skills.",
            interview_style="mathematically rigorous and engineering-driven",
            supported_difficulty_levels=["mid", "senior"],
            focus_areas=["Statistics", "ML Algorithms", "Feature Engineering", "Model Deployment"],
            system_context=(
                "You are Dr. Elena Rostova, a Lead Machine Learning Engineer. "
                "Your style is mathematically precise and production-oriented. "
                "You evaluate statistics, classical and deep machine learning algorithms, model training pipelines, and scaling systems in production. "
                "Ask questions that test both deep mathematical intuition and the practicalities of ML systems engineering."
            )
        ),
        PersonaORM(
            id=PersonaType.PROFESSOR.value,
            user_id=system_user_id,
            name="Prof. Arthur Pendelton",
            role="Computer Science Professor",
            description="An academic interviewer who focuses on first principles, theoretical foundations, and formal correctness.",
            interview_style="intellectual, theoretical, and conceptually demanding",
            supported_difficulty_levels=["junior", "mid", "senior"],
            focus_areas=["Theoretical CS", "Math Foundations", "Complexity Theory", "Formal Proofs"],
            system_context=(
                "You are Prof. Arthur Pendelton, a Computer Science Professor. "
                "Your style is highly intellectual, conceptual, and demanding of academic precision. "
                "You focus on theoretical foundations, computational complexity, discrete math, and explaining issues from first principles. "
                "Ask questions that test deep conceptual understanding and theoretical correctness rather than specific framework APIs."
            )
        ),
        PersonaORM(
            id=PersonaType.INVESTOR.value,
            user_id=system_user_id,
            name="Marcus Vance",
            role="Startup Investor & Venture Partner",
            description="An entrepreneur-turned-investor evaluating business trade-offs, quick delivery, and system scaling.",
            interview_style="strategic, pragmatic, and business-focused",
            supported_difficulty_levels=["senior"],
            focus_areas=["Business Viability", "Technical Debt", "Product-Market Fit", "Rapid Scaling"],
            system_context=(
                "You are Marcus Vance, a Venture Partner and tech investor. "
                "Your style is strategic, business-driven, and pragmatic. "
                "You evaluate how technical decisions map to business goals, trade-offs of speed vs. architecture quality, product scaling potential, and product-market fit. "
                "Ask questions about product decisions, architecture scalability under high traffic, and pragmatism in handling technical debt."
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


def test_persona_visibility_and_isolation() -> None:
    client = TestClient(app)

    # 1. Register and login User A
    user_a_payload = {
        "email": "usera@example.com",
        "full_name": "User A",
        "password": "passwordA123"
    }
    resp = client.post("/api/v1/auth/register", json=user_a_payload)
    assert resp.status_code == 201

    login_a_payload = {
        "username": user_a_payload["email"],
        "password": user_a_payload["password"]
    }
    resp = client.post("/api/v1/auth/login", data=login_a_payload)
    assert resp.status_code == 200
    token_a = resp.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # 2. Register and login User B
    user_b_payload = {
        "email": "userb@example.com",
        "full_name": "User B",
        "password": "passwordB123"
    }
    resp = client.post("/api/v1/auth/register", json=user_b_payload)
    assert resp.status_code == 201

    login_b_payload = {
        "username": user_b_payload["email"],
        "password": user_b_payload["password"]
    }
    resp = client.post("/api/v1/auth/login", data=login_b_payload)
    assert resp.status_code == 200
    token_b = resp.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 3. Create custom persona owned by User A
    custom_persona_payload = {
        "id": "custom_persona_a",
        "name": "Custom Persona A",
        "role": "QA Lead",
        "description": "Custom QA reviewer",
        "interview_style": "rigorous",
        "supported_difficulty_levels": ["mid", "senior"],
        "focus_areas": ["Automation", "Security"],
        "system_context": "Test context for custom QA lead."
    }
    resp = client.post("/api/v1/personas", json=custom_persona_payload, headers=headers_a)
    assert resp.status_code == 201

    # 4. User A lists personas (should see 5 platform personas + custom_persona_a)
    resp = client.get("/api/v1/personas", headers=headers_a)
    assert resp.status_code == 200
    personas_a = resp.json()
    assert len(personas_a) == 6
    persona_ids_a = {p["id"] for p in personas_a}
    assert "hr_interviewer" in persona_ids_a
    assert "swe_interviewer" in persona_ids_a
    assert "custom_persona_a" in persona_ids_a

    # 5. User B lists personas (should see 5 platform personas, but NOT custom_persona_a)
    resp = client.get("/api/v1/personas", headers=headers_b)
    assert resp.status_code == 200
    personas_b = resp.json()
    assert len(personas_b) == 5
    persona_ids_b = {p["id"] for p in personas_b}
    assert "hr_interviewer" in persona_ids_b
    assert "swe_interviewer" in persona_ids_b
    assert "custom_persona_a" not in persona_ids_b

    # 6. User B attempts to retrieve User A's custom persona -> 404 Not Found
    resp = client.get("/api/v1/personas/custom_persona_a", headers=headers_b)
    assert resp.status_code == 404

    # 7. User A retrieves User A's custom persona -> 200 OK
    resp = client.get("/api/v1/personas/custom_persona_a", headers=headers_a)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Custom Persona A"

    # 8. User A attempts to update platform persona -> 400 Bad Request
    update_payload = {
        "name": "Sarah Updated"
    }
    resp = client.put("/api/v1/personas/hr_interviewer", json=update_payload, headers=headers_a)
    assert resp.status_code == 400

    # 9. User A attempts to delete platform persona -> 400 Bad Request
    resp = client.delete("/api/v1/personas/hr_interviewer", headers=headers_a)
    assert resp.status_code == 400
