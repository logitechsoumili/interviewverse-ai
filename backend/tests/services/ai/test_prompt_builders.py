import pytest
import json
from backend.app.services.ai.prompts.base import PromptTemplate, PromptPayload, ConversationMessage
from backend.app.services.ai.prompts.registry import PromptRegistry
from backend.app.services.ai.prompts.renderer import PromptRenderer
from backend.app.services.ai.prompts.builders import PromptBuilder
from backend.app.services.ai.prompts.exceptions import (
    PromptError,
    PromptTemplateNotFoundError,
    PromptValidationError,
)

@pytest.fixture
def registry() -> PromptRegistry:
    """Fixture providing a bootstrapped PromptRegistry."""
    return PromptRegistry(bootstrap=True)

@pytest.fixture
def renderer() -> PromptRenderer:
    """Fixture providing a PromptRenderer."""
    return PromptRenderer()

@pytest.fixture
def builder(registry: PromptRegistry, renderer: PromptRenderer) -> PromptBuilder:
    """Fixture providing a PromptBuilder."""
    return PromptBuilder(registry=registry, renderer=renderer)


# ==========================================
# PromptRegistry Tests
# ==========================================

def test_registry_bootstrap_loads_defaults(registry: PromptRegistry) -> None:
    """Verifies that registry bootstraps default templates on startup."""
    templates = registry.list_templates()
    assert "interview_generation" in templates
    assert "evaluation_generation" in templates
    assert "report_generation" in templates

def test_registry_read_only_after_bootstrap(registry: PromptRegistry) -> None:
    """Verifies registry raises PromptError when trying to register new templates after bootstrap."""
    new_template = PromptTemplate(
        name="test_template",
        system_template="Sys",
        user_template="User"
    )
    with pytest.raises(PromptError) as exc_info:
        registry.register_template(new_template)
    assert "read-only" in str(exc_info.value)

def test_registry_lookup_success(registry: PromptRegistry) -> None:
    """Verifies successful retrieval of a registered template."""
    tmpl = registry.get_template("interview_generation")
    assert isinstance(tmpl, PromptTemplate)
    assert tmpl.name == "interview_generation"
    assert "{persona_name}" in tmpl.system_template

def test_registry_lookup_missing_raises_error(registry: PromptRegistry) -> None:
    """Verifies that lookup of missing template raises PromptTemplateNotFoundError."""
    with pytest.raises(PromptTemplateNotFoundError) as exc_info:
        registry.get_template("non_existent_template")
    assert "was not found in the registry" in str(exc_info.value)

def test_registry_custom_registration_before_bootstrap() -> None:
    """Verifies registration works before bootstrap, then locks after freeze."""
    empty_registry = PromptRegistry(bootstrap=False)
    custom_template = PromptTemplate(
        name="custom",
        system_template="Sys",
        user_template="User"
    )
    empty_registry.register_template(custom_template)
    assert "custom" in empty_registry.list_templates()
    
    empty_registry.freeze()
    with pytest.raises(PromptError):
        empty_registry.register_template(custom_template)


# ==========================================
# PromptRenderer Tests
# ==========================================

def test_renderer_success(renderer: PromptRenderer) -> None:
    """Verifies rendering works correctly with valid inputs."""
    tmpl = PromptTemplate(
        name="test",
        system_template="Hello {name}",
        user_template="Prompt for {topic}"
    )
    payload = renderer.render(tmpl, {"name": "Antigravity", "topic": "AI"})
    assert payload.system_prompt == "Hello Antigravity"
    assert payload.user_prompt == "Prompt for AI"

def test_renderer_missing_variable(renderer: PromptRenderer) -> None:
    """Verifies rendering raises PromptValidationError if required variable is missing."""
    tmpl = PromptTemplate(
        name="test",
        system_template="Hello {name}",
        user_template="Prompt for {topic}"
    )
    with pytest.raises(PromptValidationError) as exc_info:
        renderer.render(tmpl, {"name": "Antigravity"})  # missing topic
    assert "Missing template variables required for rendering: topic" in str(exc_info.value)

def test_renderer_none_or_empty_variable(renderer: PromptRenderer) -> None:
    """Verifies rendering raises PromptValidationError if variable value is None or empty."""
    tmpl = PromptTemplate(
        name="test",
        system_template="Hello {name}",
        user_template="Prompt for {topic}"
    )
    with pytest.raises(PromptValidationError) as exc_info:
        renderer.render(tmpl, {"name": "Antigravity", "topic": None})
    assert "Variable 'topic' cannot be None" in str(exc_info.value)

    with pytest.raises(PromptValidationError) as exc_info:
        renderer.render(tmpl, {"name": "   ", "topic": "AI"})
    assert "Variable 'name' cannot be empty or whitespace-only" in str(exc_info.value)

def test_renderer_residual_placeholder(renderer: PromptRenderer) -> None:
    """Verifies rendering raises error if residual/extra placeholders remain in the outputs."""
    tmpl = PromptTemplate(
        name="test",
        system_template="Hello {name}",
        user_template="Prompt for {topic} and {extra_unprovided}"
    )
    # If formatting executes but doesn't replace because key wasn't in required vars,
    # it raises KeyError which maps to PromptValidationError.
    with pytest.raises(PromptValidationError) as exc_info:
        renderer.render(tmpl, {"name": "Bob", "topic": "Physics"})
    assert "Missing template variables" in str(exc_info.value)


# ==========================================
# PromptBuilder Tests
# ==========================================

def test_build_interview_prompt_success(builder: PromptBuilder) -> None:
    """Verifies successful interview prompt construction and correct output layout."""
    history = [
        ConversationMessage(role="interviewer", content="Welcome! Tell me about yourself."),
        ConversationMessage(role="candidate", content="I am a software engineer."),
    ]
    payload = builder.build_interview_prompt(
        persona_name="Tech Interviewer",
        persona_context="You evaluate Python skills.",
        topics=["FastAPI", "Pydantic"],
        history=history,
        last_response="I also know clean architecture."
    )
    assert isinstance(payload, PromptPayload)
    assert "Tech Interviewer" in payload.system_prompt
    assert "Python skills" in payload.system_prompt
    assert "FastAPI, Pydantic" in payload.system_prompt
    assert "Interviewer: Welcome! Tell me about yourself." in payload.user_prompt
    assert "Candidate: I am a software engineer." in payload.user_prompt
    assert "Candidate's last response: I also know clean architecture." in payload.user_prompt

def test_build_interview_prompt_validation_failures(builder: PromptBuilder) -> None:
    """Verifies that build_interview_prompt raises PromptValidationError on empty/whitespace parameters."""
    history = [ConversationMessage(role="interviewer", content="Hello")]
    
    with pytest.raises(PromptValidationError) as exc_info:
        builder.build_interview_prompt("", "Context", "topic", history, "Response")
    assert "persona_name" in str(exc_info.value)

    with pytest.raises(PromptValidationError) as exc_info:
        builder.build_interview_prompt("Name", "   ", "topic", history, "Response")
    assert "persona_context" in str(exc_info.value)

    with pytest.raises(PromptValidationError) as exc_info:
        builder.build_interview_prompt("Name", "Context", "topic", history, "")
    assert "last_response" in str(exc_info.value)

def test_build_interview_prompt_history_validation(builder: PromptBuilder) -> None:
    """Verifies strict validation checks on conversation history parameter."""
    # None history
    with pytest.raises(PromptValidationError) as exc_info:
        builder.build_interview_prompt("Name", "Context", "topic", None, "Response")
    assert "history" in str(exc_info.value)

    # Empty history list
    with pytest.raises(PromptValidationError) as exc_info:
        builder.build_interview_prompt("Name", "Context", "topic", [], "Response")
    assert "history cannot be empty" in str(exc_info.value)

    # Invalid list elements
    with pytest.raises(PromptValidationError) as exc_info:
        builder.build_interview_prompt("Name", "Context", "topic", ["InvalidMessageObject"], "Response")
    assert "is not a ConversationMessage instance" in str(exc_info.value)

    # Empty content in message
    with pytest.raises(ValueError): # Raised by Pydantic min_length validation on content field
        ConversationMessage(role="interviewer", content="")

def test_build_evaluation_prompt_success(builder: PromptBuilder) -> None:
    """Verifies successful evaluation prompt construction."""
    payload = builder.build_evaluation_prompt(
        persona_context="Strict reviewer",
        rubric="Correctness and performance",
        question="What is FastAPI?",
        response="An async framework."
    )
    assert isinstance(payload, PromptPayload)
    assert "Strict reviewer" in payload.system_prompt
    assert "Correctness and performance" in payload.system_prompt
    assert "Question asked: What is FastAPI?" in payload.user_prompt
    assert "Candidate's response: An async framework." in payload.user_prompt

def test_build_evaluation_prompt_validation_failures(builder: PromptBuilder) -> None:
    """Verifies validation failures for evaluation prompts."""
    with pytest.raises(PromptValidationError):
        builder.build_evaluation_prompt("   ", "Rubric", "Q", "A")
    with pytest.raises(PromptValidationError):
        builder.build_evaluation_prompt("Context", "", "Q", "A")

def test_build_report_prompt_success(builder: PromptBuilder) -> None:
    """Verifies successful report prompt construction."""
    payload = builder.build_report_prompt(
        persona_context="Hiring Manager",
        evaluation_history=["Eval 1: Pass", "Eval 2: High Pass"]
    )
    assert isinstance(payload, PromptPayload)
    assert "Hiring Manager" in payload.system_prompt
    assert "Eval 1: Pass" in payload.user_prompt
    assert "Eval 2: High Pass" in payload.user_prompt

def test_build_report_prompt_validation_failures(builder: PromptBuilder) -> None:
    """Verifies validation failures for report prompts."""
    with pytest.raises(PromptValidationError):
        builder.build_report_prompt("Context", [])
    with pytest.raises(PromptValidationError):
        builder.build_report_prompt("Context", ["", "Eval 2"])


# ==========================================
# Serialization Tests
# ==========================================

def test_conversation_message_serialization() -> None:
    """Verifies that ConversationMessage Pydantic model serializes/deserializes successfully to/from JSON."""
    msg = ConversationMessage(role="interviewer", content="Tell me about yourself.")
    serialized = msg.model_dump_json()
    
    # Ensure correct JSON format
    data = json.loads(serialized)
    assert data["role"] == "interviewer"
    assert data["content"] == "Tell me about yourself."
    
    # Deserialize
    deserialized = ConversationMessage.model_validate_json(serialized)
    assert deserialized.role == msg.role
    assert deserialized.content == msg.content

def test_prompt_payload_serialization() -> None:
    """Verifies that PromptPayload Pydantic model serializes/deserializes successfully to/from JSON."""
    payload = PromptPayload(system_prompt="You are a guide.", user_prompt="Help me.")
    serialized = payload.model_dump_json()
    
    # Ensure correct JSON format
    data = json.loads(serialized)
    assert data["system_prompt"] == "You are a guide."
    assert data["user_prompt"] == "Help me."
    
    # Deserialize
    deserialized = PromptPayload.model_validate_json(serialized)
    assert deserialized.system_prompt == payload.system_prompt
    assert deserialized.user_prompt == payload.user_prompt
