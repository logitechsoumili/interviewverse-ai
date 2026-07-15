import pytest
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock

from backend.app.main import app
from backend.app.api.dependencies import get_gemini_service
from backend.app.services.ai.gemini.service import GeminiService
from backend.app.services.ai.personas.models import PersonaType
from backend.app.services.ai.conversation.dependencies import get_conversation_repository
from backend.app.services.ai.interview.dependencies import get_interview_repository
from backend.app.services.ai.evaluation.dependencies import get_evaluation_repository
from backend.app.services.ai.evaluation.service import EvaluationService
from backend.app.api.dependencies import get_evaluation_service, get_current_user

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
    with TestClient(app, raise_server_exceptions=True) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.mark.anyio
async def test_restart_persistence_and_evaluation(
    client: TestClient,
    mock_gemini_client: MagicMock,
) -> None:
    # 1. Start an interview session via client request (which uses DB session under the hood)
    mock_gemini_client.generate_content.return_value = "What is polymorphism in object-oriented programming?"
    start_resp = client.post("/api/v1/interviews/start", json={"persona_id": "swe_interviewer"})
    assert start_resp.status_code == 200
    interview_id = start_resp.json()["interview_id"]
    
    # 2. Exchange messaging turns via client request
    mock_gemini_client.generate_content.return_value = "Can you explain the difference between a list and a tuple in Python?"
    msg_resp = client.post(f"/api/v1/interviews/{interview_id}/message", json={"message": "Polymorphism answer."})
    assert msg_resp.status_code == 200
    
    # Complete the interview
    complete_resp = client.post(f"/api/v1/interviews/{interview_id}/complete")
    assert complete_resp.status_code == 200
    
    # 3. Simulate Server Restart / Service Recreation
    # We retrieve the db session local generator used by tests to get a clean connection
    from backend.tests.conftest import TestingSessionLocal
    db = TestingSessionLocal()
    
    try:
        # Create fresh transient repository instances linked to the new DB session
        from backend.app.services.ai.conversation.repository import ConversationRepository
        from backend.app.services.ai.interview.repository import InterviewRepository
        
        fresh_conv_repo = ConversationRepository(db=db)
        fresh_int_repo = InterviewRepository(db=db)
        
        # 4. Assert that conversation history still exists in the database
        session = fresh_conv_repo.get_session(interview_id)
        assert session.session_id == interview_id
        assert len(session.turns) == 3
        assert session.turns[0].content == "What is polymorphism in object-oriented programming?"
        assert session.turns[1].content == "Polymorphism answer."
        assert session.turns[2].content == "Can you explain the difference between a list and a tuple in Python?"
        assert session.is_active is False
        
        # 5. Verify that evaluation still succeeds using the fresh database context
        # Mock Gemini evaluation JSON payload
        mock_gemini_client.generate_content.return_value = """
        {
          "scores": {
            "overall_score": 92,
            "communication_score": 90,
            "technical_score": 94,
            "confidence_score": 92
          },
          "summary": {
            "strengths": ["Strong understanding of Polymorphism"],
            "weaknesses": ["None"],
            "recommendations": ["Hire"],
            "learning_roadmap": ["Keep learning"]
          }
        }
        """
        
        from backend.app.services.ai.personas.repository import PersonaRepository
        from backend.app.services.ai.personas.service import PersonaService
        from backend.app.services.ai.conversation.service import ConversationService
        from backend.app.services.ai.prompts.builders import PromptBuilder
        from backend.app.services.ai.prompts.registry import PromptRegistry
        from backend.app.services.ai.prompts.renderer import PromptRenderer
        from backend.app.services.ai.evaluation.repository import EvaluationRepository
        
        persona_repo = PersonaRepository(db=db)
        persona_service = PersonaService(repository=persona_repo)
        conversation_service = ConversationService(repository=fresh_conv_repo)
        
        registry = PromptRegistry()
        renderer = PromptRenderer()
        prompt_builder = PromptBuilder(registry=registry, renderer=renderer)
        
        from backend.app.services.ai.gemini.service import GeminiService
        from backend.app.core.config import get_settings
        settings = get_settings()
        gemini_service = GeminiService(client=mock_gemini_client, model=settings.GEMINI_MODEL, temperature=0.0)
        
        evaluation_repo = EvaluationRepository(db=db)
        
        evaluation_service = EvaluationService(
            prompt_builder=prompt_builder,
            gemini_service=gemini_service,
            conversation_service=conversation_service,
            persona_service=persona_service,
            interview_repository=fresh_int_repo,
            evaluation_repository=evaluation_repo
        )
        
        # Enforce system user uuid ownership consistent with conftest.py
        user_uuid = uuid.UUID("00000000-0000-0000-0000-000000000000")
        
        # Run evaluation using recreated services
        evaluation_result = await evaluation_service.evaluate_interview(interview_id, user_id=user_uuid)
        
        assert evaluation_result.scores.overall_score == 92
        assert evaluation_result.scores.technical_score == 94
        assert evaluation_result.summary.strengths == ["Strong understanding of Polymorphism"]
        
    finally:
        db.close()
