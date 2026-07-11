from typing import Optional

class PersonaError(Exception):
    """Base exception for all persona-related errors."""
    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.original_error = original_error

class PersonaNotFoundError(PersonaError):
    """Raised when a requested persona is not found."""
    pass

class InvalidPersonaError(PersonaError):
    """Raised when a persona definition is invalid or corrupt."""
    pass
