from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from backend.app.services.ai.conversation.repository import ConversationRepository, db_session_var

_conversation_repository: Optional[ConversationRepository] = None

def get_conversation_repository(db: Session = Depends(get_db)) -> ConversationRepository:
    """FastAPI-ready provider function that returns a singleton ConversationRepository instance,
    safely setting the request-scoped database session inside task-local storage to avoid mutable shared state.
    """
    global _conversation_repository
    if _conversation_repository is None:
        _conversation_repository = ConversationRepository()
        
    actual_db = db if db is not None and hasattr(db, "execute") else None
    db_session_var.set(actual_db)
    
    return _conversation_repository


