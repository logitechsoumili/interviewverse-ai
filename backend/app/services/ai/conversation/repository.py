import uuid
import hashlib
from typing import Dict, Optional, List
from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.models.interview_session import InterviewSession as InterviewSessionORM
from app.models.message import Message as MessageORM
from backend.app.services.ai.personas.models import PersonaType
from backend.app.services.ai.conversation.models import ConversationSession, ConversationTurn, SpeakerType
from backend.app.services.ai.conversation.exceptions import ConversationNotFoundError, InvalidConversationError

def to_uuid(id_str: str) -> UUID:
    """Helper to convert string ID to UUID, with deterministic fallback for test strings."""
    try:
        return uuid.UUID(id_str)
    except ValueError:
        hex_digest = hashlib.md5(id_str.encode('utf-8')).hexdigest()
        return uuid.UUID(hex_digest)

class ConversationRepository:
    """Hybrid repository for technical interview conversations.
    
    Supports database persistence via SQLAlchemy Session if provided, otherwise
    falls back to in-memory dictionary.
    """
    
    def __init__(self, db: Optional[Session] = None) -> None:
        # Instance level db session (only populated for transient test instances)
        self._db = db
        self._sessions: Dict[str, ConversationSession] = {}

    @property
    def db(self) -> Optional[Session]:
        """Resolves the database session from the instance variable."""
        return self._db

    def _is_db_active(self) -> bool:
        """Checks if active DB session is available."""
        resolved_db = self.db
        return resolved_db is not None and hasattr(resolved_db, "execute")

    def create_session(self, session_id: str, persona_id: PersonaType | str) -> ConversationSession:
        """Creates and stores a new ConversationSession.
        
        Raises:
            InvalidConversationError: If session_id is empty or session already exists.
        """
        if not session_id or not session_id.strip():
            raise InvalidConversationError("Session ID cannot be empty or whitespace.")
            
        if self._is_db_active():
            db_id = to_uuid(session_id)
            stmt = select(InterviewSessionORM).where(InterviewSessionORM.id == db_id)
            if self.db.execute(stmt).scalar_one_or_none():
                raise InvalidConversationError(f"Session with ID '{session_id}' already exists.")
                
        if session_id in self._sessions:
            raise InvalidConversationError(f"Session with ID '{session_id}' already exists.")
            
        session = ConversationSession(session_id=session_id, persona_id=persona_id)
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> ConversationSession:
        """Retrieves a ConversationSession by ID.
        
        Raises:
            ConversationNotFoundError: If session doesn't exist.
            InvalidConversationError: If session_id parameter is invalid.
        """
        if not session_id or not session_id.strip():
            raise InvalidConversationError("Session ID cannot be empty or whitespace.")
            
        if self._is_db_active():
            db_id = to_uuid(session_id)
            stmt = select(InterviewSessionORM).where(InterviewSessionORM.id == db_id)
            db_sess = self.db.execute(stmt).scalar_one_or_none()
            if db_sess:
                turns = []
                for msg in db_sess.messages:
                    turns.append(ConversationTurn(
                        role=SpeakerType(msg.sender),
                        content=msg.content,
                        timestamp=msg.timestamp
                    ))
                
                try:
                    p_id = PersonaType(db_sess.persona_id)
                except ValueError:
                    p_id = PersonaType.SWE  # Fallback for custom persona
                    
                session = ConversationSession(
                    session_id=str(db_sess.id),
                    persona_id=p_id,
                    turns=turns,
                    is_active=(db_sess.status != "completed"),
                    created_at=db_sess.created_at
                )
                self._sessions[session_id] = session
                return session
            
        if session_id not in self._sessions:
            raise ConversationNotFoundError(f"Session with ID '{session_id}' was not found.")
        return self._sessions[session_id]

    def append_turn(self, session_id: str, turn: ConversationTurn) -> None:
        """Appends a turn to the session's turns list.
        
        Raises:
            ConversationNotFoundError: If session doesn't exist.
        """
        if not session_id or not session_id.strip():
            raise InvalidConversationError("Session ID cannot be empty or whitespace.")
            
        db_written = False
        if self._is_db_active():
            db_id = to_uuid(session_id)
            stmt = select(InterviewSessionORM).where(InterviewSessionORM.id == db_id)
            db_sess = self.db.execute(stmt).scalar_one_or_none()
            if db_sess:
                db_message = MessageORM(
                    id=uuid.uuid4(),
                    session_id=db_id,
                    sender=turn.role.value if hasattr(turn.role, 'value') else str(turn.role),
                    content=turn.content,
                    timestamp=turn.timestamp
                )
                self.db.add(db_message)
                self.db.commit()
                db_written = True

        if session_id in self._sessions:
            self._sessions[session_id].turns.append(turn)
        elif not db_written:
            raise ConversationNotFoundError(f"Session with ID '{session_id}' was not found.")

    def delete_session(self, session_id: str) -> None:
        """Deletes a session's messages from the repository.
        
        Raises:
            ConversationNotFoundError: If session doesn't exist.
            InvalidConversationError: If session_id parameter is invalid.
        """
        if not session_id or not session_id.strip():
            raise InvalidConversationError("Session ID cannot be empty or whitespace.")
            
        deleted = False
        
        if self._is_db_active():
            db_id = to_uuid(session_id)
            stmt = select(InterviewSessionORM).where(InterviewSessionORM.id == db_id)
            db_sess = self.db.execute(stmt).scalar_one_or_none()
            if db_sess:
                del_stmt = delete(MessageORM).where(MessageORM.session_id == db_id)
                self.db.execute(del_stmt)
                self.db.commit()
                deleted = True

        if session_id in self._sessions:
            del self._sessions[session_id]
            deleted = True
            
        if not deleted:
            raise ConversationNotFoundError(f"Session with ID '{session_id}' was not found.")


