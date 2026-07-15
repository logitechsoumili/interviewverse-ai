from fastapi import Depends

# Import repositories
from backend.app.services.ai.conversation.repository import ConversationRepository
from backend.app.services.ai.interview.repository import InterviewRepository
from backend.app.services.ai.evaluation.repository import EvaluationRepository
from backend.app.services.ai.personas.repository import PersonaRepository

# Import repository providers
from backend.app.services.ai.conversation.dependencies import get_conversation_repository
from backend.app.services.ai.interview.dependencies import get_interview_repository
from backend.app.services.ai.evaluation.dependencies import get_evaluation_repository
from backend.app.services.ai.personas.dependencies import get_persona_repository

# Import services
from backend.app.services.ai.conversation.service import ConversationService
from backend.app.services.ai.interview.service import InterviewService
from backend.app.services.ai.evaluation.service import EvaluationService
from backend.app.services.ai.personas.service import PersonaService
from backend.app.services.ai.reports.service import ReportService

# Import prompt builders and Gemini service dependencies
from backend.app.services.ai.prompts.builders import PromptBuilder
from backend.app.services.ai.prompts.registry import PromptRegistry
from backend.app.services.ai.prompts.renderer import PromptRenderer
from backend.app.services.ai.gemini.service import GeminiService
from backend.app.services.ai.gemini.dependencies import get_gemini_service

# Dependency Providers

def get_persona_service(
    repository: PersonaRepository = Depends(get_persona_repository),
) -> PersonaService:
    """Dependency provider that instantiates and returns a PersonaService."""
    return PersonaService(repository=repository)

def get_conversation_service(
    repository: ConversationRepository = Depends(get_conversation_repository),
) -> ConversationService:
    """Dependency provider that instantiates and returns a ConversationService."""
    return ConversationService(repository=repository)

def get_prompt_builder() -> PromptBuilder:
    """Dependency provider that instantiates and returns a PromptBuilder."""
    registry = PromptRegistry()
    renderer = PromptRenderer()
    return PromptBuilder(registry=registry, renderer=renderer)

def get_interview_service(
    persona_service: PersonaService = Depends(get_persona_service),
    conversation_service: ConversationService = Depends(get_conversation_service),
    prompt_builder: PromptBuilder = Depends(get_prompt_builder),
    gemini_service: GeminiService = Depends(get_gemini_service),
    repository: InterviewRepository = Depends(get_interview_repository),
) -> InterviewService:
    """Dependency provider that instantiates and returns an InterviewService."""
    return InterviewService(
        persona_service=persona_service,
        conversation_service=conversation_service,
        prompt_builder=prompt_builder,
        gemini_service=gemini_service,
        repository=repository,
    )

def get_evaluation_service(
    prompt_builder: PromptBuilder = Depends(get_prompt_builder),
    gemini_service: GeminiService = Depends(get_gemini_service),
    conversation_service: ConversationService = Depends(get_conversation_service),
    persona_service: PersonaService = Depends(get_persona_service),
    interview_repository: InterviewRepository = Depends(get_interview_repository),
    evaluation_repository: EvaluationRepository = Depends(get_evaluation_repository),
) -> EvaluationService:
    """Dependency provider that instantiates and returns an EvaluationService."""
    return EvaluationService(
        prompt_builder=prompt_builder,
        gemini_service=gemini_service,
        conversation_service=conversation_service,
        persona_service=persona_service,
        interview_repository=interview_repository,
        evaluation_repository=evaluation_repository,
    )

def get_report_service(
    interview_repository: InterviewRepository = Depends(get_interview_repository),
    persona_service: PersonaService = Depends(get_persona_service),
    evaluation_repository: EvaluationRepository = Depends(get_evaluation_repository),
) -> ReportService:
    """Dependency provider that instantiates and returns a ReportService."""
    return ReportService(
        interview_repository=interview_repository,
        persona_service=persona_service,
        evaluation_repository=evaluation_repository,
    )
