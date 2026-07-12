from fastapi import APIRouter, Depends
from typing import List

from backend.app.services.ai.personas.service import PersonaService
from backend.app.services.ai.personas.models import PersonaType
from backend.app.api.dependencies import get_persona_service
from backend.app.schemas.personas import PersonaListItemSchema, PersonaDetailSchema

router = APIRouter(prefix="/api/v1/personas", tags=["Personas"])

@router.get("", response_model=List[PersonaListItemSchema])
def get_personas(service: PersonaService = Depends(get_persona_service)) -> List[PersonaListItemSchema]:
    """Retrieves all bootstrapped interviewer personas."""
    personas = service.list_personas()
    return [
        PersonaListItemSchema(id=p.id.value, name=p.name, role=p.role)
        for p in personas
    ]

@router.get("/{persona_id}", response_model=PersonaDetailSchema)
def get_persona(
    persona_id: PersonaType,
    service: PersonaService = Depends(get_persona_service),
) -> PersonaDetailSchema:
    """Retrieves the details of a single interviewer persona."""
    persona = service.get_persona(persona_id)
    return PersonaDetailSchema(
        id=persona.id.value,
        name=persona.name,
        role=persona.role,
        description=persona.description,
        interview_style=persona.interview_style,
        supported_difficulty_levels=persona.supported_difficulty_levels,
        focus_areas=persona.focus_areas,
    )
