from typing import List, Optional
from uuid import UUID
from backend.app.services.ai.personas.models import Persona, PersonaType, PersonaPromptContext
from backend.app.services.ai.personas.repository import PersonaRepository
from backend.app.services.ai.personas.exceptions import PersonaNotFoundError, InvalidPersonaError

class PersonaService:
    """Service layer managing interviewer personas and enforcing user ownership/data isolation."""
    
    def __init__(self, repository: PersonaRepository) -> None:
        """Initializes the service with constructor-injected repository.
        
        Args:
            repository: Persona repository.
        """
        self.repository = repository

    def _validate_persona(self, persona: Persona) -> None:
        """Performs validation checks on persona properties."""
        if not persona.id:
            raise InvalidPersonaError("Persona definition has an empty ID.")
        if not persona.name or not persona.name.strip():
            raise InvalidPersonaError(f"Persona '{persona.id}' has an empty or whitespace name.")
        if not persona.role or not persona.role.strip():
            raise InvalidPersonaError(f"Persona '{persona.id}' has an empty or whitespace role.")
        if not persona.interview_style or not persona.interview_style.strip():
            raise InvalidPersonaError(f"Persona '{persona.id}' has an empty or whitespace interview_style.")
        if not persona.system_context or not persona.system_context.strip():
            raise InvalidPersonaError(f"Persona '{persona.id}' has an empty or whitespace system_context.")

    def get_persona(self, persona_id: str | PersonaType, user_id: Optional[UUID] = None) -> Persona:
        """Retrieves a persona by ID and verifies user ownership.
        
        Raises:
            PersonaNotFoundError: If requested persona is not found or belongs to another user.
            InvalidPersonaError: If persona definition fails validation checks.
        """
        if not self.repository.db and not isinstance(persona_id, PersonaType):
            raise InvalidPersonaError("Invalid persona_type. Must be a PersonaType enum value.")
            
        try:
            persona = self.repository.get_persona(persona_id, user_id)
        except PersonaNotFoundError as e:
            raise PersonaNotFoundError(f"Persona '{persona_id}' not found.", original_error=e) from e

        self._validate_persona(persona)
        return persona

    def list_personas(self, user_id: Optional[UUID] = None) -> List[Persona]:
        """Returns all personas owned by the current user."""
        return self.repository.list_personas(user_id)

    def create_persona(self, user_id: Optional[UUID] = None, persona: Optional[Persona] = None) -> Persona:
        """Creates a new persona owned by the current user."""
        if not user_id:
            import uuid
            user_id = uuid.UUID("00000000-0000-0000-0000-000000000000")
        self._validate_persona(persona)
        return self.repository.create_persona(user_id, persona)

    def update_persona(self, user_id: Optional[UUID] = None, persona_id: Optional[str] = None, persona: Optional[Persona] = None) -> Persona:
        """Updates an existing persona owned by the current user."""
        if not user_id:
            import uuid
            user_id = uuid.UUID("00000000-0000-0000-0000-000000000000")
        self._validate_persona(persona)
        return self.repository.update_persona(user_id, persona_id, persona)

    def delete_persona(self, user_id: Optional[UUID] = None, persona_id: Optional[str] = None) -> None:
        """Deletes a persona owned by the current user."""
        if not user_id:
            import uuid
            user_id = uuid.UUID("00000000-0000-0000-0000-000000000000")
        # Check existence first
        self.get_persona(persona_id, user_id)
        self.repository.delete_persona(user_id, persona_id)

    def get_prompt_context(self, persona_id: str | PersonaType, user_id: Optional[UUID] = None) -> PersonaPromptContext:
        """Exposes persona information formatted for prompt building contexts.
        
        Enforces user ownership boundaries.
        """
        persona = self.get_persona(persona_id, user_id)
        focus_str = ", ".join(persona.focus_areas)
        difficulty_str = ", ".join(persona.supported_difficulty_levels)
        
        persona_context = (
            f"Interviewer Name: {persona.name}. "
            f"Role: {persona.role}. "
            f"Style: {persona.interview_style}. "
            f"Supported Difficulty: {difficulty_str}. "
            f"Focus Areas: {focus_str}. "
            f"Instruction: {persona.system_context}"
        )
        return PersonaPromptContext(
            persona_name=persona.name,
            persona_context=persona_context
        )
