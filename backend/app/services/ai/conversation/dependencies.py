from typing import Optional
from backend.app.services.ai.conversation.repository import ConversationRepository

_conversation_repository: Optional[ConversationRepository] = None

def get_conversation_repository() -> ConversationRepository:
    """FastAPI-ready provider function that returns a singleton ConversationRepository instance."""
    global _conversation_repository
    if _conversation_repository is None:
        _conversation_repository = ConversationRepository()
    return _conversation_repository
