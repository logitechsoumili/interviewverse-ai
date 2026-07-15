import hashlib
import uuid
import contextvars
from typing import Dict, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.app.services.ai.evaluation.models import EvaluationResult, EvaluationScore, EvaluationSummary
from backend.app.services.ai.evaluation.exceptions import (
    EvaluationNotFoundError,
    InvalidEvaluationError,
)
from app.models.evaluation import Evaluation as EvaluationORM

# Thread/Task-local storage for the active SQLAlchemy Session to avoid mutating singleton instances
db_session_var: contextvars.ContextVar[Optional[Session]] = contextvars.ContextVar("evaluation_db_session", default=None)

def to_uuid(id_str: str) -> UUID:
    """Helper to convert string ID to UUID, with deterministic fallback for test strings."""
    try:
        return uuid.UUID(id_str)
    except ValueError:
        hex_digest = hashlib.md5(id_str.encode('utf-8')).hexdigest()
        return uuid.UUID(hex_digest)

class EvaluationRepository:
    """Hybrid repository for storing and retrieving EvaluationResult objects.
    
    Supports database persistence via SQLAlchemy Session if provided, otherwise
    falls back to in-memory dictionary.
    """

    def __init__(self, db: Optional[Session] = None) -> None:
        self._db = db
        self._evaluations: Dict[str, EvaluationResult] = {}

    @property
    def db(self) -> Optional[Session]:
        """Resolves the database session from task-local context or instance variable fallback."""
        context_db = db_session_var.get()
        if context_db is not None:
            return context_db
        return self._db

    def save_evaluation(self, interview_id: str, evaluation: EvaluationResult, user_id: Optional[UUID] = None) -> EvaluationResult:
        """Stores or updates an EvaluationResult."""
        if not interview_id or not interview_id.strip():
            raise InvalidEvaluationError("Interview ID cannot be empty or whitespace.")
        if evaluation is None:
            raise InvalidEvaluationError("Evaluation cannot be None.")

        if self.db:
            db_session_id = to_uuid(interview_id)
            if not user_id:
                user_id = to_uuid("00000000-0000-0000-0000-000000000000")
            
            # Check if evaluation already exists
            stmt = select(EvaluationORM).where(EvaluationORM.session_id == db_session_id)
            db_eval = self.db.execute(stmt).scalar_one_or_none()
            
            if not db_eval:
                db_eval = EvaluationORM(
                    id=uuid.uuid4(),
                    session_id=db_session_id,
                    user_id=user_id,
                    overall_score=evaluation.scores.overall_score,
                    communication_score=evaluation.scores.communication_score,
                    technical_score=evaluation.scores.technical_score,
                    confidence_score=evaluation.scores.confidence_score,
                    strengths=evaluation.summary.strengths,
                    weaknesses=evaluation.summary.weaknesses,
                    recommendations=evaluation.summary.recommendations,
                    learning_roadmap=evaluation.summary.learning_roadmap,
                    evaluated_at=evaluation.evaluated_at,
                )
                self.db.add(db_eval)
            else:
                db_eval.overall_score = evaluation.scores.overall_score
                db_eval.communication_score = evaluation.scores.communication_score
                db_eval.technical_score = evaluation.scores.technical_score
                db_eval.confidence_score = evaluation.scores.confidence_score
                db_eval.strengths = evaluation.summary.strengths
                db_eval.weaknesses = evaluation.summary.weaknesses
                db_eval.recommendations = evaluation.summary.recommendations
                db_eval.learning_roadmap = evaluation.summary.learning_roadmap
                db_eval.evaluated_at = evaluation.evaluated_at

            self.db.commit()
            return evaluation
        else:
            self._evaluations[interview_id.strip()] = evaluation
            return evaluation

    def get_evaluation(self, interview_id: str, user_id: Optional[UUID] = None) -> EvaluationResult:
        """Retrieves an EvaluationResult by interview ID, enforcing user ownership."""
        if not interview_id or not interview_id.strip():
            raise InvalidEvaluationError("Interview ID cannot be empty or whitespace.")

        if self.db:
            db_session_id = to_uuid(interview_id)
            stmt = select(EvaluationORM).where(EvaluationORM.session_id == db_session_id)
            if user_id:
                stmt = stmt.where(EvaluationORM.user_id == user_id)
                
            db_eval = self.db.execute(stmt).scalar_one_or_none()
            if not db_eval:
                raise EvaluationNotFoundError(f"Evaluation for interview '{interview_id}' was not found.")
                
            from backend.app.services.ai.personas.models import PersonaType
            
            # Since persona_id was stored in interview session, we can fetch it, 
            # or default to MLE if the enum doesn't map. 
            # In our DB model, evaluation doesn't store persona_id, but the schema requires it.
            # We can retrieve the persona_id from the corresponding interview_session table.
            from app.models.interview_session import InterviewSession as InterviewSessionORM
            persona_id_str = "swe_interviewer"
            sess_stmt = select(InterviewSessionORM).where(InterviewSessionORM.id == db_session_id)
            db_sess = self.db.execute(sess_stmt).scalar_one_or_none()
            if db_sess:
                persona_id_str = db_sess.persona_id

            return EvaluationResult(
                scores=EvaluationScore(
                    overall_score=db_eval.overall_score,
                    communication_score=db_eval.communication_score,
                    technical_score=db_eval.technical_score,
                    confidence_score=db_eval.confidence_score,
                ),
                summary=EvaluationSummary(
                    strengths=db_eval.strengths,
                    weaknesses=db_eval.weaknesses,
                    recommendations=db_eval.recommendations,
                    learning_roadmap=db_eval.learning_roadmap,
                ),
                evaluated_at=db_eval.evaluated_at,
                persona_id=PersonaType(persona_id_str),
            )
        else:
            key = interview_id.strip()
            if key not in self._evaluations:
                raise EvaluationNotFoundError(f"Evaluation for interview '{interview_id}' was not found.")
            return self._evaluations[key]

    def delete_evaluation(self, interview_id: str, user_id: Optional[UUID] = None) -> None:
        """Deletes an EvaluationResult from the repository."""
        if not interview_id or not interview_id.strip():
            raise InvalidEvaluationError("Interview ID cannot be empty or whitespace.")

        if self.db:
            db_session_id = to_uuid(interview_id)
            stmt = select(EvaluationORM).where(EvaluationORM.session_id == db_session_id)
            if user_id:
                stmt = stmt.where(EvaluationORM.user_id == user_id)
                
            db_eval = self.db.execute(stmt).scalar_one_or_none()
            if not db_eval:
                raise EvaluationNotFoundError(f"Evaluation for interview '{interview_id}' was not found.")
                
            self.db.delete(db_eval)
            self.db.commit()
        else:
            key = interview_id.strip()
            if key not in self._evaluations:
                raise EvaluationNotFoundError(f"Evaluation for interview '{interview_id}' was not found.")
            del self._evaluations[key]
