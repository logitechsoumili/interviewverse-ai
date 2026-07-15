import hashlib
import uuid
from typing import Dict, Optional
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.app.services.ai.interview.models import InterviewSession, InterviewStatus
from backend.app.services.ai.interview.exceptions import InterviewNotFoundError, InterviewError
from app.models.interview_session import InterviewSession as InterviewSessionORM

def to_uuid(id_str: str) -> UUID:
    """Helper to convert string ID to UUID, with deterministic fallback for test strings."""
    try:
        return uuid.UUID(id_str)
    except ValueError:
        # Deterministic UUID generation for arbitrary test string IDs (like "session-123")
        hex_digest = hashlib.md5(id_str.encode('utf-8')).hexdigest()
        return uuid.UUID(hex_digest)

class InterviewRepository:
    """Hybrid repository for technical interview sessions.
    
    Supports database persistence via SQLAlchemy Session if provided, otherwise
    falls back to in-memory dictionary.
    """
    
    def __init__(self, db: Optional[Session] = None) -> None:
        self.db = db
        self._interviews: Dict[str, InterviewSession] = {}

    def create_interview(self, session: InterviewSession) -> InterviewSession:
        """Stores a new InterviewSession."""
        if not session.interview_id or not session.interview_id.strip():
            raise InterviewError("Interview ID cannot be empty.")
            
        if self.db:
            db_id = to_uuid(session.interview_id)
            # Check duplicate
            stmt = select(InterviewSessionORM).where(InterviewSessionORM.id == db_id)
            if self.db.execute(stmt).scalar_one_or_none():
                raise InterviewError(f"Interview session '{session.interview_id}' already exists.")
                
            db_session = InterviewSessionORM(
                id=db_id,
                user_id=session.user_id if session.user_id else to_uuid("00000000-0000-0000-0000-000000000000"),
                persona_id=session.persona_id.value if hasattr(session.persona_id, 'value') else str(session.persona_id),
                topics=session.topics,
                difficulty=session.difficulty,
                status=session.status.value if hasattr(session.status, 'value') else str(session.status),
                created_at=session.created_at,
                completed_at=session.completed_at,
            )
            self.db.add(db_session)
            self.db.commit()
            return session
        else:
            if session.interview_id in self._interviews:
                raise InterviewError(f"Interview session '{session.interview_id}' already exists.")
            self._interviews[session.interview_id] = session
            return session

    def get_interview(self, interview_id: str, user_id: Optional[UUID] = None) -> InterviewSession:
        """Retrieves an InterviewSession by ID, filtered by user_id if DB is active."""
        if not interview_id or not interview_id.strip():
            raise InterviewError("Interview ID cannot be empty.")
            
        if self.db:
            db_id = to_uuid(interview_id)
            stmt = select(InterviewSessionORM).where(InterviewSessionORM.id == db_id)
            if user_id:
                stmt = stmt.where(InterviewSessionORM.user_id == user_id)
                
            db_session = self.db.execute(stmt).scalar_one_or_none()
            if not db_session:
                raise InterviewNotFoundError(f"Interview session '{interview_id}' was not found.")
                
            return InterviewSession(
                interview_id=str(db_session.id),
                session_id=str(db_session.id),
                persona_id=db_session.persona_id,
                user_id=db_session.user_id,
                status=InterviewStatus(db_session.status),
                topics=db_session.topics,
                difficulty=db_session.difficulty,
                created_at=db_session.created_at,
                completed_at=db_session.completed_at,
            )
        else:
            if interview_id not in self._interviews:
                raise InterviewNotFoundError(f"Interview session '{interview_id}' was not found.")
            session = self._interviews[interview_id]
            if user_id and session.user_id != user_id:
                raise InterviewNotFoundError(f"Interview session '{interview_id}' was not found.")
            return session

    def update_interview(self, session: InterviewSession) -> InterviewSession:
        """Updates an existing InterviewSession."""
        if not session.interview_id or not session.interview_id.strip():
            raise InterviewError("Interview ID cannot be empty.")
            
        if self.db:
            db_id = to_uuid(session.interview_id)
            sess_user_id = session.user_id if session.user_id else to_uuid("00000000-0000-0000-0000-000000000000")
            stmt = select(InterviewSessionORM).where(InterviewSessionORM.id == db_id, InterviewSessionORM.user_id == sess_user_id)
            db_session = self.db.execute(stmt).scalar_one_or_none()
            if not db_session:
                raise InterviewNotFoundError(f"Interview session '{session.interview_id}' was not found.")
                
            db_session.status = session.status.value if hasattr(session.status, 'value') else str(session.status)
            db_session.topics = session.topics
            db_session.difficulty = session.difficulty
            db_session.completed_at = session.completed_at
            
            self.db.commit()
            return session
        else:
            self.get_interview(session.interview_id, session.user_id)  # verifies existence/ownership
            self._interviews[session.interview_id] = session
            return session

    def complete_interview(self, interview_id: str, user_id: Optional[UUID] = None) -> InterviewSession:
        """Marks an interview session as completed."""
        session = self.get_interview(interview_id, user_id)
        session.status = InterviewStatus.COMPLETED
        session.completed_at = datetime.now(timezone.utc)
        self.update_interview(session)
        return session

    def delete_interview(self, interview_id: str, user_id: Optional[UUID] = None) -> None:
        """Deletes an interview session from the repository."""
        if not interview_id or not interview_id.strip():
            raise InterviewError("Interview ID cannot be empty.")
            
        if self.db:
            db_id = to_uuid(interview_id)
            stmt = select(InterviewSessionORM).where(InterviewSessionORM.id == db_id)
            if user_id:
                stmt = stmt.where(InterviewSessionORM.user_id == user_id)
                
            db_session = self.db.execute(stmt).scalar_one_or_none()
            if not db_session:
                raise InterviewNotFoundError(f"Interview session '{interview_id}' was not found.")
                
            self.db.delete(db_session)
            self.db.commit()
        else:
            if interview_id not in self._interviews:
                raise InterviewNotFoundError(f"Interview session '{interview_id}' was not found.")
            session = self._interviews[interview_id]
            if user_id and session.user_id != user_id:
                raise InterviewNotFoundError(f"Interview session '{interview_id}' was not found.")
            del self._interviews[interview_id]

    def list_interviews(self, user_id: UUID) -> list[InterviewSession]:
        """Lists all interview sessions for a specific user."""
        if self.db:
            stmt = select(InterviewSessionORM).where(InterviewSessionORM.user_id == user_id)
            db_sessions = self.db.execute(stmt).scalars().all()
            from backend.app.services.ai.personas.models import PersonaType
            return [
                InterviewSession(
                    interview_id=str(db_session.id),
                    session_id=str(db_session.id),
                    persona_id=PersonaType(db_session.persona_id) if hasattr(PersonaType, 'value') else db_session.persona_id,
                    user_id=db_session.user_id,
                    status=InterviewStatus(db_session.status),
                    topics=db_session.topics,
                    difficulty=db_session.difficulty,
                    created_at=db_session.created_at,
                    completed_at=db_session.completed_at,
                )
                for db_session in db_sessions
            ]
        else:
            return [
                sess
                for sess in self._interviews.values()
                if sess.user_id == user_id
            ]
