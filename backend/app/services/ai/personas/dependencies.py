from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.services.ai.personas.repository import PersonaRepository, db_session_var
from app.db.session import get_db

_persona_repository: Optional[PersonaRepository] = None

def get_persona_repository(db: Session = Depends(get_db)) -> PersonaRepository:
    """FastAPI-ready provider function that returns a singleton PersonaRepository instance,
    safely setting the request-scoped database session inside task-local storage to avoid mutable shared state.
    """
    global _persona_repository
    if _persona_repository is None:
        _persona_repository = PersonaRepository()
    
    actual_db = db if db is not None and hasattr(db, "execute") else None
    db_session_var.set(actual_db)
    return _persona_repository
