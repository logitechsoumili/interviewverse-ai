from typing import Optional

class PromptError(Exception):
    """Base exception for all prompt management errors."""
    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.original_error = original_error

class PromptTemplateNotFoundError(PromptError):
    """Raised when a requested prompt template is not found in the registry."""
    pass

class PromptValidationError(PromptError):
    """Raised when validation of input parameters/variables for prompt templates fails."""
    pass
