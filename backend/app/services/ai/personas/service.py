from typing import List
from backend.app.services.ai.personas.models import Persona, PersonaType, PersonaPromptContext
from backend.app.services.ai.personas.repository import PersonaRepository
from backend.app.services.ai.personas.exceptions import PersonaNotFoundError, InvalidPersonaError

class PersonaService:
    """Service layer managing interviewer personas and preparing them for prompt generation."""
    
    def __init__(self, repository: PersonaRepository) -> None:
        """Initializes the service with constructor-injected repository.
        
        Args:
            repository: In-memory persona repository.
        """
        self.repository = repository

    def _validate_persona(self, persona: Persona) -> None:
        """Performs check validation on persona definition model properties."""
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

    def get_persona(self, persona_type: PersonaType) -> Persona:
        """Retrieves a persona by PersonaType enum.
        
        Raises:
            PersonaNotFoundError: If requested persona is not found.
            InvalidPersonaError: If persona definition fails validation checks or if key is invalid.
        """
        if not isinstance(persona_type, PersonaType):
            raise InvalidPersonaError("Invalid persona_type. Must be a PersonaType enum value.")
            
        try:
            persona = self.repository.get_persona(persona_type)
        except PersonaNotFoundError as e:
            raise PersonaNotFoundError(f"Persona '{persona_type}' not found.", original_error=e) from e

        # Validate structure integrity
        self._validate_persona(persona)
        return persona

    def list_personas(self) -> List[Persona]:
        """Returns all available bootstrapped personas."""
        return self.repository.list_personas()

    def get_prompt_context(self, persona_type: PersonaType) -> PersonaPromptContext:
        """Exposes persona information formatted for prompt building contexts.
        
        Exposes structured metadata in a generic way, keeping it decoupled from builders.
        
        Returns:
            A PersonaPromptContext Pydantic object.
        """
        persona = self.get_persona(persona_type)
        focus_str = ", ".join(persona.focus_areas)
        difficulty_str = ", ".join(persona.supported_difficulty_levels)
        
        # Build prompt context generically
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
