from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.services.ai.interview.repository import InterviewRepository
from app.db.session import get_db

_interview_repository: Optional[InterviewRepository] = None

def get_interview_repository(db: Session = Depends(get_db)) -> InterviewRepository:
    """FastAPI-ready provider function that returns a singleton InterviewRepository instance."""
    global _interview_repository
    if _interview_repository is None:
        _interview_repository = InterviewRepository(db=db)
    else:
        _interview_repository.db = db
    return _interview_repository
