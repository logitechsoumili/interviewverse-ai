from typing import List, Optional
from datetime import datetime, timezone
from difflib import SequenceMatcher

from backend.app.services.ai.prompts.base import ConversationMessage
from backend.app.services.ai.personas.models import PersonaType
from backend.app.services.ai.conversation.models import ConversationSession, ConversationTurn, SpeakerType
from backend.app.services.ai.conversation.repository import ConversationRepository
from backend.app.services.ai.conversation.exceptions import (
    ConversationNotFoundError,
    InvalidConversationError,
)

class ConversationService:
    """Service layer managing interview conversation sessions, history, and validations."""
    
    DEFAULT_SIMILARITY_THRESHOLD: float = 0.8

    def __init__(self, repository: ConversationRepository) -> None:
        """Initializes the service with constructor-injected repository.
        
        Args:
            repository: In-memory conversation repository.
        """
        self.repository = repository

    def _validate_session_id(self, session_id: str) -> None:
        """Validates that session ID is present and not empty."""
        if not session_id or not session_id.strip():
            raise InvalidConversationError("Session ID cannot be empty or whitespace.")

    def _validate_content(self, content: str) -> None:
        """Validates that message content is present and not empty."""
        if not content or not content.strip():
            raise InvalidConversationError("Message content cannot be empty or whitespace.")

    def create_session(self, session_id: str, persona_id: str | PersonaType) -> ConversationSession:
        """Creates a new interview conversation session.
        
        Args:
            session_id: Unique session identifier.
            persona_id: Persona ID string or PersonaType enum value.
            
        Returns:
            The created ConversationSession.
        """
        self._validate_session_id(session_id)
        id_str = persona_id.value if isinstance(persona_id, PersonaType) else str(persona_id)
        if not id_str or not id_str.strip():
            raise InvalidConversationError("persona_id must be a non-empty string or a valid PersonaType enum value.")
        return self.repository.create_session(session_id, persona_id)

    def append_interviewer_turn(self, session_id: str, content: str) -> None:
        """Appends an interviewer turn to the session."""
        self._validate_session_id(session_id)
        self._validate_content(content)
        
        # Verify session exists
        self.repository.get_session(session_id)
        
        turn = ConversationTurn(
            role=SpeakerType.INTERVIEWER,
            content=content.strip(),
            timestamp=datetime.now(timezone.utc)
        )
        self.repository.append_turn(session_id, turn)

    def append_candidate_turn(self, session_id: str, content: str) -> None:
        """Appends a candidate turn to the session."""
        self._validate_session_id(session_id)
        self._validate_content(content)
        
        # Verify session exists
        self.repository.get_session(session_id)
        
        turn = ConversationTurn(
            role=SpeakerType.CANDIDATE,
            content=content.strip(),
            timestamp=datetime.now(timezone.utc)
        )
        self.repository.append_turn(session_id, turn)

    def retrieve_conversation_history(self, session_id: str) -> List[ConversationTurn]:
        """Retrieves the full chronological list of turns for a session."""
        self._validate_session_id(session_id)
        session = self.repository.get_session(session_id)
        return session.turns

    def build_llm_ready_history(self, session_id: str) -> List[ConversationMessage]:
        """Converts the session turns list to a simplified list of ConversationMessage objects.
        
        This format is compatible with the Prompt Architecture's history input parameter.
        """
        turns = self.retrieve_conversation_history(session_id)
        messages = []
        for turn in turns:
            messages.append(
                ConversationMessage(
                    role=turn.role.value,
                    content=turn.content
                )
            )
        return messages

    def has_similar_question(
        self,
        session_id: str,
        question: str,
        similarity_threshold: Optional[float] = None,
    ) -> bool:
        """Checks if a similar question has already been asked by the interviewer in this session.
        
        Args:
            session_id: Unique session identifier.
            question: The candidate question to check.
            similarity_threshold: Float similarity score threshold. Defaults to DEFAULT_SIMILARITY_THRESHOLD.
            
        Returns:
            True if a duplicate is found, False otherwise.
        """
        self._validate_session_id(session_id)
        self._validate_content(question)
        
        threshold = similarity_threshold if similarity_threshold is not None else self.DEFAULT_SIMILARITY_THRESHOLD
        
        turns = self.retrieve_conversation_history(session_id)
        question_norm = question.lower().strip()
        
        for turn in turns:
            if turn.role == SpeakerType.INTERVIEWER:
                existing_norm = turn.content.lower().strip()
                similarity = SequenceMatcher(None, question_norm, existing_norm).ratio()
                if similarity >= threshold:
                    return True
                    
        return False

    def get_turn_count(self, session_id: str) -> int:
        """Returns the total number of turns in the conversation session."""
        return len(self.retrieve_conversation_history(session_id))

    def get_interviewer_turn_count(self, session_id: str) -> int:
        """Returns the number of turns made by the interviewer."""
        turns = self.retrieve_conversation_history(session_id)
        return len([t for t in turns if t.role == SpeakerType.INTERVIEWER])

    def get_candidate_turn_count(self, session_id: str) -> int:
        """Returns the number of turns made by the candidate."""
        turns = self.retrieve_conversation_history(session_id)
        return len([t for t in turns if t.role == SpeakerType.CANDIDATE])
