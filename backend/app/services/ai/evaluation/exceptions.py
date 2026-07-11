from typing import Optional

class EvaluationError(Exception):
    """Base exception for all Evaluation Engine errors."""
    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.original_error = original_error

class EvaluationParsingError(EvaluationError):
    """Raised when the LLM evaluation response cannot be parsed or decoded as valid JSON."""
    pass

class InvalidEvaluationError(EvaluationError):
    """Raised when evaluation inputs or score validation rules fail."""
    pass

class EvaluationNotFoundError(EvaluationError):
    """Raised when the requested evaluation is not found."""
    pass
