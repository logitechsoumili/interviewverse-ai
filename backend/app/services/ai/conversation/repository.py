from typing import Dict, Optional, List
from backend.app.services.ai.personas.models import PersonaType
from backend.app.services.ai.conversation.models import ConversationSession, ConversationTurn
from backend.app.services.ai.conversation.exceptions import ConversationNotFoundError, InvalidConversationError

class ConversationRepository:
    """In-memory repository for storing and managing ConversationSession structures."""
    
    def __init__(self) -> None:
        self._sessions: Dict[str, ConversationSession] = {}

    def create_session(self, session_id: str, persona_id: PersonaType) -> ConversationSession:
        """Creates and stores a new ConversationSession.
        
        Raises:
            InvalidConversationError: If session_id is empty or session already exists.
        """
        if not session_id or not session_id.strip():
            raise InvalidConversationError("Session ID cannot be empty or whitespace.")
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
        if session_id not in self._sessions:
            raise ConversationNotFoundError(f"Session with ID '{session_id}' was not found.")
        return self._sessions[session_id]

    def append_turn(self, session_id: str, turn: ConversationTurn) -> None:
        """Appends a turn to the session's turns list.
        
        Raises:
            ConversationNotFoundError: If session doesn't exist.
        """
        session = self.get_session(session_id)
        session.turns.append(turn)

    def delete_session(self, session_id: str) -> None:
        """Deletes a session from the repository.
        
        Raises:
            ConversationNotFoundError: If session doesn't exist.
            InvalidConversationError: If session_id parameter is invalid.
        """
        if not session_id or not session_id.strip():
            raise InvalidConversationError("Session ID cannot be empty or whitespace.")
        if session_id not in self._sessions:
            raise ConversationNotFoundError(f"Session with ID '{session_id}' was not found.")
        del self._sessions[session_id]
