from typing import Optional

class GeminiError(Exception):
    """Base exception class for all Gemini service operations.
    
    Acts as a barrier so the rest of the application never receives raw Gemini SDK exceptions.
    """
    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.original_error = original_error

class GeminiRateLimitError(GeminiError):
    """Raised when Gemini API rate limits are exceeded (HTTP 429)."""
    pass

class GeminiAuthenticationError(GeminiError):
    """Raised when authentication or permission fails (HTTP 401, 403)."""
    pass

class GeminiGenerationError(GeminiError):
    """Raised when request arguments are invalid, resources are not found, or response is empty/malformed."""
    pass
