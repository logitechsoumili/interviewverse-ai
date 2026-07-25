from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.app.services.ai.personas.exceptions import PersonaNotFoundError, InvalidPersonaError
from backend.app.services.ai.conversation.exceptions import ConversationNotFoundError, InvalidConversationError
from backend.app.services.ai.interview.exceptions import (
    InterviewNotFoundError,
    InterviewAlreadyCompletedError,
    InterviewError,
    InterviewGenerationError,
)
from backend.app.services.ai.evaluation.exceptions import (
    EvaluationNotFoundError,
    EvaluationError,
    EvaluationParsingError,
    InvalidEvaluationError,
)
from backend.app.services.ai.reports.exceptions import (
    ReportError,
    ReportGenerationError,
    InvalidReportError,
)
from backend.app.services.ai.gemini.exceptions import (
    GeminiError,
    GeminiRateLimitError,
    GeminiAuthenticationError,
    GeminiGenerationError,
)
import logging

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI) -> None:
    """Registers exception handlers that translate domain exceptions to HTTP responses."""

    # 404 Not Found
    @app.exception_handler(PersonaNotFoundError)
    @app.exception_handler(InterviewNotFoundError)
    @app.exception_handler(ConversationNotFoundError)
    @app.exception_handler(EvaluationNotFoundError)
    async def not_found_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )

    # 409 Conflict
    @app.exception_handler(InterviewAlreadyCompletedError)
    async def conflict_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)}
        )

    # 400 Bad Request
    @app.exception_handler(InvalidPersonaError)
    @app.exception_handler(InvalidConversationError)
    @app.exception_handler(InvalidEvaluationError)
    @app.exception_handler(InvalidReportError)
    @app.exception_handler(InterviewError)
    async def bad_request_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)}
        )

    # 500 Internal Server Error (explicit domain errors)
    @app.exception_handler(InterviewGenerationError)
    @app.exception_handler(EvaluationParsingError)
    @app.exception_handler(ReportGenerationError)
    @app.exception_handler(EvaluationError)
    @app.exception_handler(ReportError)
    async def internal_server_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)}
        )

    # Upstream AI Exceptions
    @app.exception_handler(GeminiAuthenticationError)
    async def gemini_auth_handler(request: Request, exc: GeminiAuthenticationError):
        logger.error(f"Gemini authentication error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Upstream AI service authentication or configuration failed. Please check backend GEMINI_API_KEY settings."}
        )

    @app.exception_handler(GeminiRateLimitError)
    async def gemini_rate_limit_handler(request: Request, exc: GeminiRateLimitError):
        logger.warning(f"Gemini rate limit error: {str(exc)}")
        return JSONResponse(
            status_code=429,
            content={"detail": "Upstream AI service rate limit exceeded. Please try again shortly."}
        )

    @app.exception_handler(GeminiGenerationError)
    @app.exception_handler(GeminiError)
    async def gemini_general_handler(request: Request, exc: Exception):
        logger.error(f"Gemini API execution error: {str(exc)}")
        return JSONResponse(
            status_code=502,
            content={"detail": f"Upstream AI service failure: {str(exc)}"}
        )

    # Global Fallback for Unhandled Exceptions (prevents connection drops and missing CORS headers)
    @app.exception_handler(Exception)
    async def global_fallback_handler(request: Request, exc: Exception):
        logger.exception("An unhandled exception occurred during request processing")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(exc)}"}
        )
