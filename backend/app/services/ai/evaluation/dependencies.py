from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.services.ai.evaluation.repository import EvaluationRepository
from app.db.session import get_db

def get_evaluation_repository(db: Session = Depends(get_db)) -> EvaluationRepository:
    """FastAPI-ready provider function that returns a transient EvaluationRepository instance."""
    actual_db = db if db is not None and hasattr(db, "execute") else None
    return EvaluationRepository(db=actual_db)
