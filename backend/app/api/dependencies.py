from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

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

async def set_db_context(db: Session = Depends(get_db)) -> None:
    """Sets the database session context variable on the main event loop thread."""
    from backend.app.services.ai.conversation.repository import db_session_var
    actual_db = db if db is not None and hasattr(db, "execute") else None
    db_session_var.set(actual_db)

def get_conversation_service(
    repository: ConversationRepository = Depends(get_conversation_repository),
    _ctx: None = Depends(set_db_context),
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
    db: Session = Depends(get_db),
) -> ReportService:
    """Dependency provider that instantiates and returns a ReportService."""
    return ReportService(
        interview_repository=interview_repository,
        persona_service=persona_service,
        evaluation_repository=evaluation_repository,
        db=db,
    )


from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose.exceptions import ExpiredSignatureError

from app.auth.jwt import decode_access_token
from app.models.user import User
from app.services.user_service import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """Validate JWT access token and retrieve the currently authenticated User."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = UUID(user_id_str)
    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except (JWTError, ValueError) as exc:
        raise credentials_exception from exc

    user = get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user

