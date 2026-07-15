from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from backend.app.services.ai.personas.service import PersonaService
from backend.app.api.dependencies import get_persona_service, get_current_user
from backend.app.schemas.personas import (
    PersonaListItemSchema,
    PersonaDetailSchema,
    PersonaCreateSchema,
    PersonaUpdateSchema,
)
from backend.app.services.ai.personas.models import Persona as PersonaModel
from backend.app.services.ai.personas.exceptions import PersonaNotFoundError
from app.models.user import User

router = APIRouter(prefix="/api/v1/personas", tags=["Personas"])

@router.get("", response_model=List[PersonaListItemSchema])
def get_personas(
    service: PersonaService = Depends(get_persona_service),
    current_user: User = Depends(get_current_user),
) -> List[PersonaListItemSchema]:
    """Retrieves all interviewer personas owned by the current user."""
    personas = service.list_personas(user_id=current_user.id)
    return [
        PersonaListItemSchema(id=p.id if isinstance(p.id, str) else p.id.value, name=p.name, role=p.role)
        for p in personas
    ]

@router.get("/{persona_id}", response_model=PersonaDetailSchema)
def get_persona(
    persona_id: str,
    service: PersonaService = Depends(get_persona_service),
    current_user: User = Depends(get_current_user),
) -> PersonaDetailSchema:
    """Retrieves the details of a single interviewer persona owned by the current user."""
    try:
        persona = service.get_persona(persona_id, user_id=current_user.id)
    except PersonaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return PersonaDetailSchema(
        id=persona.id if isinstance(persona.id, str) else persona.id.value,
        name=persona.name,
        role=persona.role,
        description=persona.description,
        interview_style=persona.interview_style,
        supported_difficulty_levels=persona.supported_difficulty_levels,
        focus_areas=persona.focus_areas,
    )

@router.post("", response_model=PersonaDetailSchema, status_code=status.HTTP_201_CREATED)
def create_persona(
    payload: PersonaCreateSchema,
    service: PersonaService = Depends(get_persona_service),
    current_user: User = Depends(get_current_user),
) -> PersonaDetailSchema:
    """Creates a custom persona owned by the current user."""
    # Enforce ownership in service layer by parsing payload into schema model
    model = PersonaModel(
        id=payload.id,
        name=payload.name,
        role=payload.role,
        description=payload.description,
        interview_style=payload.interview_style,
        supported_difficulty_levels=payload.supported_difficulty_levels,
        focus_areas=payload.focus_areas,
        system_context=payload.system_context,
    )
    persona = service.create_persona(user_id=current_user.id, persona=model)
    return PersonaDetailSchema(
        id=persona.id if isinstance(persona.id, str) else persona.id.value,
        name=persona.name,
        role=persona.role,
        description=persona.description,
        interview_style=persona.interview_style,
        supported_difficulty_levels=persona.supported_difficulty_levels,
        focus_areas=persona.focus_areas,
    )

@router.put("/{persona_id}", response_model=PersonaDetailSchema)
def update_persona(
    persona_id: str,
    payload: PersonaUpdateSchema,
    service: PersonaService = Depends(get_persona_service),
    current_user: User = Depends(get_current_user),
) -> PersonaDetailSchema:
    """Updates a custom persona owned by the current user."""
    # First, verify existence & ownership (will raise 404 if not owned)
    try:
        existing = service.get_persona(persona_id, user_id=current_user.id)
    except PersonaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    # Construct the update
    model = PersonaModel(
        id=persona_id,
        name=payload.name if payload.name is not None else existing.name,
        role=payload.role if payload.role is not None else existing.role,
        description=payload.description if payload.description is not None else existing.description,
        interview_style=payload.interview_style if payload.interview_style is not None else existing.interview_style,
        supported_difficulty_levels=payload.supported_difficulty_levels if payload.supported_difficulty_levels is not None else existing.supported_difficulty_levels,
        focus_areas=payload.focus_areas if payload.focus_areas is not None else existing.focus_areas,
        system_context=payload.system_context if payload.system_context is not None else existing.system_context,
    )
    
    updated = service.update_persona(user_id=current_user.id, persona_id=persona_id, persona=model)
    return PersonaDetailSchema(
        id=updated.id if isinstance(updated.id, str) else updated.id.value,
        name=updated.name,
        role=updated.role,
        description=updated.description,
        interview_style=updated.interview_style,
        supported_difficulty_levels=updated.supported_difficulty_levels,
        focus_areas=updated.focus_areas,
    )

@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(
    persona_id: str,
    service: PersonaService = Depends(get_persona_service),
    current_user: User = Depends(get_current_user),
) -> None:
    """Deletes a custom persona owned by the current user."""
    try:
        service.delete_persona(user_id=current_user.id, persona_id=persona_id)
    except PersonaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
