from typing import Optional

class InterviewError(Exception):
    """Base exception for all interview engine errors."""
    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.original_error = original_error

class InterviewNotFoundError(InterviewError):
    """Raised when an interview session cannot be found in the repository."""
    pass

class InterviewAlreadyCompletedError(InterviewError):
    """Raised when an action is attempted on an already completed interview."""
    pass

class InterviewGenerationError(InterviewError):
    """Raised when question generation fails (e.g. duplicate checks fail repeatedly)."""
    pass
