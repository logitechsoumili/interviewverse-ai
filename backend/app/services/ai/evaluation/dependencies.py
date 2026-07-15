from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.services.ai.evaluation.repository import EvaluationRepository, db_session_var
from app.db.session import get_db

_evaluation_repository: Optional[EvaluationRepository] = None

def get_evaluation_repository(db: Session = Depends(get_db)) -> EvaluationRepository:
    """FastAPI-ready provider function that returns a singleton EvaluationRepository instance,
    safely setting the request-scoped database session inside task-local storage to avoid mutable shared state.
    """
    global _evaluation_repository
    if _evaluation_repository is None:
        _evaluation_repository = EvaluationRepository()
    
    actual_db = db if db is not None and hasattr(db, "execute") else None
    db_session_var.set(actual_db)
    return _evaluation_repository
