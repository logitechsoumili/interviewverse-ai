from typing import Optional

class ConversationError(Exception):
    """Base exception for all conversation management errors."""
    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.original_error = original_error

class ConversationNotFoundError(ConversationError):
    """Raised when a requested conversation session is not found."""
    pass

class InvalidConversationError(ConversationError):
    """Raised when conversation parameters fail validation checks."""
    pass
