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
