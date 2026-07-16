from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.services.ai.personas.repository import PersonaRepository
from app.db.session import get_db

def get_persona_repository(db: Session = Depends(get_db)) -> PersonaRepository:
    """FastAPI-ready provider function that returns a transient PersonaRepository instance."""
    actual_db = db if db is not None and hasattr(db, "execute") else None
    return PersonaRepository(db=actual_db)
