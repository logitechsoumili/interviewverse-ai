from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.services.ai.evaluation.repository import EvaluationRepository
from app.db.session import get_db

_evaluation_repository: Optional[EvaluationRepository] = None

def get_evaluation_repository(db: Session = Depends(get_db)) -> EvaluationRepository:
    """FastAPI-ready provider function that returns a singleton EvaluationRepository instance."""
    global _evaluation_repository
    if _evaluation_repository is None:
        _evaluation_repository = EvaluationRepository(db=db)
    else:
        _evaluation_repository.db = db
    return _evaluation_repository
