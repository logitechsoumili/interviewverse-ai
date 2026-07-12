from typing import Optional
from backend.app.services.ai.personas.repository import PersonaRepository

_persona_repository: Optional[PersonaRepository] = None

def get_persona_repository() -> PersonaRepository:
    """FastAPI-ready provider function that returns a singleton PersonaRepository instance."""
    global _persona_repository
    if _persona_repository is None:
        _persona_repository = PersonaRepository()
    return _persona_repository
