from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from backend.app.services.ai.conversation.repository import ConversationRepository

def get_conversation_repository(db: Session = Depends(get_db)) -> ConversationRepository:
    """FastAPI-ready provider function that returns a transient ConversationRepository instance."""
    actual_db = db if db is not None and hasattr(db, "execute") else None
    return ConversationRepository(db=actual_db)
