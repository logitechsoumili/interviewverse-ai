from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.services.ai.interview.repository import InterviewRepository, db_session_var
from app.db.session import get_db

_interview_repository: Optional[InterviewRepository] = None

def get_interview_repository(db: Session = Depends(get_db)) -> InterviewRepository:
    """FastAPI-ready provider function that returns a singleton InterviewRepository instance,
    safely setting the request-scoped database session inside task-local storage to avoid mutable shared state.
    """
    global _interview_repository
    if _interview_repository is None:
        _interview_repository = InterviewRepository()
    
    actual_db = db if db is not None and hasattr(db, "execute") else None
    db_session_var.set(actual_db)
    return _interview_repository
