from typing import Optional

class ReportError(Exception):
    """Base exception for all Report Generation Engine errors."""
    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.original_error = original_error

class ReportGenerationError(ReportError):
    """Raised when report generation fails due to logical or processing issues."""
    pass

class InvalidReportError(ReportError):
    """Raised when report inputs, sections, or output validation rules fail."""
    pass
