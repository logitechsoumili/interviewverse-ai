from typing import Dict
from backend.app.services.ai.evaluation.models import EvaluationResult
from backend.app.services.ai.evaluation.exceptions import (
    EvaluationNotFoundError,
    InvalidEvaluationError,
)

class EvaluationRepository:
    """In-memory repository for storing and retrieving EvaluationResult objects."""

    def __init__(self) -> None:
        self._evaluations: Dict[str, EvaluationResult] = {}

    def save_evaluation(self, interview_id: str, evaluation: EvaluationResult) -> EvaluationResult:
        """Stores or updates an EvaluationResult in-memory.
        
        Args:
            interview_id: Unique identifier for the interview session.
            evaluation: The EvaluationResult instance.
            
        Returns:
            The saved EvaluationResult.
            
        Raises:
            InvalidEvaluationError: If interview_id is empty/whitespace or evaluation is None.
        """
        if not interview_id or not interview_id.strip():
            raise InvalidEvaluationError("Interview ID cannot be empty or whitespace.")
        if evaluation is None:
            raise InvalidEvaluationError("Evaluation cannot be None.")

        self._evaluations[interview_id.strip()] = evaluation
        return evaluation

    def get_evaluation(self, interview_id: str) -> EvaluationResult:
        """Retrieves an EvaluationResult by interview ID.
        
        Args:
            interview_id: Unique identifier for the interview session.
            
        Returns:
            The stored EvaluationResult.
            
        Raises:
            InvalidEvaluationError: If interview_id is empty/whitespace.
            EvaluationNotFoundError: If the evaluation does not exist.
        """
        if not interview_id or not interview_id.strip():
            raise InvalidEvaluationError("Interview ID cannot be empty or whitespace.")

        key = interview_id.strip()
        if key not in self._evaluations:
            raise EvaluationNotFoundError(f"Evaluation for interview '{interview_id}' was not found.")
        return self._evaluations[key]

    def delete_evaluation(self, interview_id: str) -> None:
        """Deletes an EvaluationResult from the repository.
        
        Args:
            interview_id: Unique identifier for the interview session.
            
        Raises:
            InvalidEvaluationError: If interview_id is empty/whitespace.
            EvaluationNotFoundError: If the evaluation does not exist.
        """
        if not interview_id or not interview_id.strip():
            raise InvalidEvaluationError("Interview ID cannot be empty or whitespace.")

        key = interview_id.strip()
        if key not in self._evaluations:
            raise EvaluationNotFoundError(f"Evaluation for interview '{interview_id}' was not found.")
        del self._evaluations[key]
