from typing import Optional
from backend.app.services.ai.interview.repository import InterviewRepository

_interview_repository: Optional[InterviewRepository] = None

def get_interview_repository() -> InterviewRepository:
    """FastAPI-ready provider function that returns a singleton InterviewRepository instance."""
    global _interview_repository
    if _interview_repository is None:
        _interview_repository = InterviewRepository()
    return _interview_repository
