from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.services.ai.personas.repository import PersonaRepository
from app.db.session import get_db

_persona_repository: Optional[PersonaRepository] = None

def get_persona_repository(db: Session = Depends(get_db)) -> PersonaRepository:
    """FastAPI-ready provider function that returns a singleton PersonaRepository instance."""
    global _persona_repository
    if _persona_repository is None:
        _persona_repository = PersonaRepository(db=db)
    else:
        _persona_repository.db = db
    return _persona_repository
