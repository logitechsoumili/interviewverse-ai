import os
import pytest
import uuid
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db

DB_FILE = "test.db"
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


def register_global_override(dependency, override_callable):
    """Utility to register a dependency override on all instances of app in sys.modules."""
    # Register on the imported app instance
    app.dependency_overrides[dependency] = override_callable
    
    # Register on any other app instances loaded via different import paths
    for name, module in list(sys.modules.items()):
        if name.endswith('app.main') and hasattr(module, 'app'):
            module.app.dependency_overrides[dependency] = override_callable


def clear_global_overrides():
    """Utility to clear dependency overrides on all instances of app in sys.modules."""
    app.dependency_overrides.clear()
    for name, module in list(sys.modules.items()):
        if name.endswith('app.main') and hasattr(module, 'app'):
            module.app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def setup_db():
    # Clean up previous test database if it exists
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
        except PermissionError:
            pass

    # Create tables in the test DB
    Base.metadata.create_all(bind=engine)
    
    # 1. Insert the mock user into the test database to prevent FK violations
    mock_user_id = uuid.UUID("00000000-0000-0000-0000-000000000000")
    from app.models.user import User as UserORM
    db = TestingSessionLocal()
    
    existing_user = db.query(UserORM).filter(UserORM.id == mock_user_id).first()
    if not existing_user:
        mock_user_db = UserORM(
            id=mock_user_id,
            email="system@interviewverse.ai",
            full_name="System User",
            password_hash="disabled"
        )
        db.add(mock_user_db)
    
    # 2. Seed default personas for this mock user so lookups succeed
    from app.models.persona import Persona as PersonaORM
    from backend.app.services.ai.personas.models import PersonaType
    
    default_personas = [
        PersonaORM(
            id=PersonaType.HR.value,
            user_id=mock_user_id,
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
            user_id=mock_user_id,
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
            user_id=mock_user_id,
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
            user_id=mock_user_id,
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
            user_id=mock_user_id,
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
    for persona in default_personas:
        existing_p = db.query(PersonaORM).filter(PersonaORM.id == persona.id, PersonaORM.user_id == mock_user_id).first()
        if not existing_p:
            db.add(persona)
        
    db.commit()
    db.close()
    
    # 3. Register dependency overrides on all app instances for all possible import paths
    # Resolve get_db path variations
    try:
        from app.db.session import get_db as get_db1
        register_global_override(get_db1, override_get_db)
    except ImportError:
        pass
    try:
        from backend.app.db.session import get_db as get_db2
        register_global_override(get_db2, override_get_db)
    except ImportError:
        pass

    # Resolve get_current_user path variations
    from app.models.user import User
    mock_user = User(
        id=mock_user_id,
        email="system@interviewverse.ai",
        full_name="System User"
    )
    
    try:
        from app.api.dependencies import get_current_user as get_current_user1
        register_global_override(get_current_user1, lambda: mock_user)
    except ImportError:
        pass
    try:
        from backend.app.api.dependencies import get_current_user as get_current_user2
        register_global_override(get_current_user2, lambda: mock_user)
    except ImportError:
        pass
        
    yield
    
    # Clean up overrides
    clear_global_overrides()
    
    # Close connection pool to release file locks
    engine.dispose()
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
        except PermissionError:
            pass
