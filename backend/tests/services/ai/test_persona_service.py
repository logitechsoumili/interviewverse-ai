import pytest
import json
from backend.app.services.ai.personas.models import Persona, PersonaType, PersonaPromptContext
from backend.app.services.ai.personas.repository import PersonaRepository
from backend.app.services.ai.personas.service import PersonaService
from backend.app.services.ai.personas.exceptions import (
    PersonaNotFoundError,
    InvalidPersonaError,
)
from backend.app.services.ai.prompts.builders import PromptBuilder
from backend.app.services.ai.prompts.registry import PromptRegistry
from backend.app.services.ai.prompts.renderer import PromptRenderer
from backend.app.services.ai.prompts.base import ConversationMessage

@pytest.fixture
def repository() -> PersonaRepository:
    """Fixture providing a default PersonaRepository."""
    return PersonaRepository()

@pytest.fixture
def service(repository: PersonaRepository) -> PersonaService:
    """Fixture providing a default PersonaService."""
    return PersonaService(repository=repository)


# ==========================================
# PersonaRepository & Bootstrap Tests
# ==========================================

def test_repository_bootstrap_loads_all_personas(repository: PersonaRepository) -> None:
    """Verifies that all 5 required personas are loaded into the repository."""
    personas = repository.list_personas()
    assert len(personas) == 5
    
    loaded_ids = {p.id for p in personas}
    expected_ids = {
        PersonaType.HR,
        PersonaType.SWE,
        PersonaType.MLE,
        PersonaType.PROFESSOR,
        PersonaType.INVESTOR,
    }
    assert loaded_ids == expected_ids

def test_repository_get_persona_success(repository: PersonaRepository) -> None:
    """Verifies successful retrieval of a persona by ID."""
    persona = repository.get_persona(PersonaType.HR)
    assert persona.name == "Sarah Jenkins"
    assert persona.id == PersonaType.HR
    assert "Behavioral" in persona.focus_areas
    assert persona.interview_style == "warm, conversational, and highly empathetic"
    assert persona.supported_difficulty_levels == ["junior", "mid", "senior"]

def test_repository_get_persona_missing_raises_error(repository: PersonaRepository) -> None:
    """Verifies lookup of missing ID raises PersonaNotFoundError."""
    with pytest.raises(PersonaNotFoundError) as exc_info:
        repository.get_persona("non_existent_id")  # type: ignore
    assert "was not found" in str(exc_info.value)

def test_repository_exists(repository: PersonaRepository) -> None:
    """Verifies exists check works correctly."""
    assert repository.exists(PersonaType.SWE) is True
    assert repository.exists("unknown") is False  # type: ignore

def test_repository_bootstrap_validation_fails_on_duplicates() -> None:
    """Verifies repository bootstrap raises InvalidPersonaError if duplicate IDs exist."""
    item = Persona.model_construct(
        id=PersonaType.HR,
        name="Jenkins",
        role="Interviewer",
        description="Desc",
        interview_style="warm",
        supported_difficulty_levels=["mid"],
        focus_areas=["Behavioral"],
        system_context="Sys"
    )
    with pytest.raises(InvalidPersonaError) as exc_info:
        PersonaRepository(raw_list=[item, item])
    assert "Duplicate persona ID detected" in str(exc_info.value)

def test_repository_bootstrap_validation_fails_on_empty_name() -> None:
    """Verifies repository bootstrap raises InvalidPersonaError if name is empty."""
    bad_persona = Persona.model_construct(
        id=PersonaType.HR,
        name="",  # empty name
        role="Interviewer",
        description="Desc",
        interview_style="warm",
        supported_difficulty_levels=["mid"],
        focus_areas=["Behavioral"],
        system_context="Sys"
    )
    with pytest.raises(InvalidPersonaError) as exc_info:
        PersonaRepository(raw_list=[bad_persona])
    assert "empty or whitespace name" in str(exc_info.value)

def test_repository_bootstrap_validation_fails_on_empty_focus_areas() -> None:
    """Verifies repository bootstrap raises InvalidPersonaError if focus_areas is empty."""
    bad_persona = Persona.model_construct(
        id=PersonaType.HR,
        name="Sarah",
        role="Interviewer",
        description="Desc",
        interview_style="warm",
        supported_difficulty_levels=["mid"],
        focus_areas=[],  # empty list
        system_context="Sys"
    )
    with pytest.raises(InvalidPersonaError) as exc_info:
        PersonaRepository(raw_list=[bad_persona])
    assert "empty focus_areas list" in str(exc_info.value)

def test_repository_bootstrap_validation_fails_on_empty_context() -> None:
    """Verifies repository bootstrap raises InvalidPersonaError if system_context is empty."""
    bad_persona = Persona.model_construct(
        id=PersonaType.HR,
        name="Sarah",
        role="Interviewer",
        description="Desc",
        interview_style="warm",
        supported_difficulty_levels=["mid"],
        focus_areas=["Behavioral"],
        system_context="   "  # whitespace only
    )
    with pytest.raises(InvalidPersonaError) as exc_info:
        PersonaRepository(raw_list=[bad_persona])
    assert "empty or whitespace system_context" in str(exc_info.value)



# ==========================================
# PersonaService Tests
# ==========================================

def test_service_get_persona_success(service: PersonaService) -> None:
    """Verifies successful retrieval of validated persona from service."""
    persona = service.get_persona(PersonaType.SWE)
    assert persona.id == PersonaType.SWE
    assert persona.name == "Alex Rivera"

def test_service_get_persona_invalid_type_raises_error(service: PersonaService) -> None:
    """Verifies that lookup with string ID instead of PersonaType raises InvalidPersonaError."""
    with pytest.raises(InvalidPersonaError) as exc_info:
        service.get_persona("hr_interviewer")  # type: ignore
    assert "Must be a PersonaType enum value" in str(exc_info.value)

def test_service_get_prompt_context_formatting(service: PersonaService) -> None:
    """Verifies prompt context string formatting is correct and contains style/difficulty details."""
    context_obj = service.get_prompt_context(PersonaType.INVESTOR)
    assert isinstance(context_obj, PersonaPromptContext)
    assert context_obj.persona_name == "Marcus Vance"
    
    ctx = context_obj.persona_context
    assert "Interviewer Name: Marcus Vance" in ctx
    assert "Role: Startup Investor & Venture Partner" in ctx
    assert "Style: strategic, pragmatic, and business-focused" in ctx
    assert "Supported Difficulty: senior" in ctx
    assert "Focus Areas: Business Viability, Technical Debt, Product-Market Fit, Rapid Scaling" in ctx
    assert "Instruction:" in ctx

def test_service_list_personas(service: PersonaService) -> None:
    """Verifies list operation returns all available personas."""
    lst = service.list_personas()
    assert len(lst) == 5
    assert all(isinstance(p, Persona) for p in lst)


# ==========================================
# Prompt Integration Test Simulation
# ==========================================

def test_prompt_builder_integration(service: PersonaService) -> None:
    """Simulates integration by resolving prompt context and feeding it into PromptBuilder."""
    # Resolve persona prompt context metadata
    prompt_context = service.get_prompt_context(PersonaType.SWE)
    
    # Initialize PromptBuilder dependencies
    prompt_registry = PromptRegistry(bootstrap=True)
    prompt_renderer = PromptRenderer()
    builder = PromptBuilder(registry=prompt_registry, renderer=prompt_renderer)
    
    # Run interview generation builder
    history = [
        ConversationMessage(role="interviewer", content="Welcome! Let's start with binary trees."),
    ]
    payload = builder.build_interview_prompt(
        persona_name=prompt_context.persona_name,
        persona_context=prompt_context.persona_context,
        topics=["Data Structures", "Recursion"],
        history=history,
        last_response="I am ready."
    )
    
    # Confirm prompts contain correct persona parameters
    assert prompt_context.persona_name in payload.system_prompt
    assert "Style: analytical, technical, and highly structured" in payload.system_prompt
    assert "Recursion" in payload.system_prompt


# ==========================================
# Serialization Tests
# ==========================================

def test_persona_serialization(service: PersonaService) -> None:
    """Verifies that Persona Pydantic model serializes and validates correctly from JSON."""
    persona = service.get_persona(PersonaType.MLE)
    serialized = persona.model_dump_json()
    
    # Decode and verify keys
    data = json.loads(serialized)
    assert data["id"] == "mle_interviewer"
    assert data["name"] == "Dr. Elena Rostova"
    assert data["interview_style"] == "mathematically rigorous and engineering-driven"
    
    # Load back
    deserialized = Persona.model_validate_json(serialized)
    assert deserialized.id == persona.id
    assert deserialized.name == persona.name
    assert deserialized.supported_difficulty_levels == persona.supported_difficulty_levels

def test_persona_prompt_context_serialization(service: PersonaService) -> None:
    """Verifies that PersonaPromptContext Pydantic model serializes and validates correctly from JSON."""
    context_obj = service.get_prompt_context(PersonaType.PROFESSOR)
    serialized = context_obj.model_dump_json()
    
    data = json.loads(serialized)
    assert data["persona_name"] == "Prof. Arthur Pendelton"
    assert "Computer Science Professor" in data["persona_context"]
    
    # Load back
    deserialized = PersonaPromptContext.model_validate_json(serialized)
    assert deserialized.persona_name == context_obj.persona_name
    assert deserialized.persona_context == context_obj.persona_context
