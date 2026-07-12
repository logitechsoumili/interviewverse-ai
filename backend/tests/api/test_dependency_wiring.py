from unittest.mock import MagicMock
from backend.app.api.dependencies import (
    get_persona_service,
    get_conversation_service,
    get_prompt_builder,
    get_interview_service,
    get_evaluation_service,
    get_report_service,
)
from backend.app.services.ai.personas.repository import PersonaRepository
from backend.app.services.ai.conversation.repository import ConversationRepository
from backend.app.services.ai.interview.repository import InterviewRepository
from backend.app.services.ai.evaluation.repository import EvaluationRepository
from backend.app.services.ai.gemini.service import GeminiService

def test_dependency_wiring_resolves() -> None:
    """Verifies that all dependency provider functions construct service layers properly."""
    persona_repo = PersonaRepository()
    conv_repo = ConversationRepository()
    interview_repo = InterviewRepository()
    eval_repo = EvaluationRepository()
    gemini_svc = MagicMock(spec=GeminiService)
    
    # 1. PersonaService
    persona_svc = get_persona_service(persona_repo)
    assert persona_svc.repository is persona_repo
    
    # 2. ConversationService
    conv_svc = get_conversation_service(conv_repo)
    assert conv_svc.repository is conv_repo
    
    # 3. PromptBuilder
    builder = get_prompt_builder()
    assert builder.registry is not None
    assert builder.renderer is not None
    
    # 4. InterviewService
    int_svc = get_interview_service(
        persona_service=persona_svc,
        conversation_service=conv_svc,
        prompt_builder=builder,
        gemini_service=gemini_svc,
        repository=interview_repo,
    )
    assert int_svc.repository is interview_repo
    
    # 5. EvaluationService
    eval_svc = get_evaluation_service(
        prompt_builder=builder,
        gemini_service=gemini_svc,
        conversation_service=conv_svc,
        persona_service=persona_svc,
        interview_repository=interview_repo,
        evaluation_repository=eval_repo,
    )
    assert eval_svc.evaluation_repository is eval_repo
    
    # 6. ReportService
    rep_svc = get_report_service(
        interview_repository=interview_repo,
        persona_service=persona_svc,
        evaluation_repository=eval_repo,
    )
    assert rep_svc.evaluation_repository is eval_repo
    assert rep_svc.persona_service is persona_svc
    assert rep_svc.interview_repository is interview_repo
