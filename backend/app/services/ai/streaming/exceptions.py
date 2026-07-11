from typing import Optional

class StreamingError(Exception):
    """Base exception for all streaming engine errors."""
    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.original_error = original_error

class InvalidStreamError(StreamingError):
    """Raised when stream data or chunks are invalid (e.g. empty, corrupt, bad sequences)."""
    pass

class StreamInterruptedError(StreamingError):
    """Raised when a stream is cut short or fails mid-stream."""
    pass
