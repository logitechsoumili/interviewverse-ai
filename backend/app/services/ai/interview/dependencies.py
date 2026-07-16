from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.services.ai.interview.repository import InterviewRepository
from app.db.session import get_db

def get_interview_repository(db: Session = Depends(get_db)) -> InterviewRepository:
    """FastAPI-ready provider function that returns a transient InterviewRepository instance."""
    actual_db = db if db is not None and hasattr(db, "execute") else None
    return InterviewRepository(db=actual_db)
