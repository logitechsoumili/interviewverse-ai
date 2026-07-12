from typing import Optional
from backend.app.services.ai.evaluation.repository import EvaluationRepository

_evaluation_repository: Optional[EvaluationRepository] = None

def get_evaluation_repository() -> EvaluationRepository:
    """FastAPI-ready provider function that returns a singleton EvaluationRepository instance."""
    global _evaluation_repository
    if _evaluation_repository is None:
        _evaluation_repository = EvaluationRepository()
    return _evaluation_repository
