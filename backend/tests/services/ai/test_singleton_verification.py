from backend.app.services.ai.conversation.dependencies import get_conversation_repository
from backend.app.services.ai.interview.dependencies import get_interview_repository
from backend.app.services.ai.evaluation.dependencies import get_evaluation_repository
from backend.app.services.ai.personas.dependencies import get_persona_repository

def test_conversation_repository_singleton() -> None:
    repo1 = get_conversation_repository()
    repo2 = get_conversation_repository()
    assert repo1 is repo2

def test_interview_repository_singleton() -> None:
    repo1 = get_interview_repository()
    repo2 = get_interview_repository()
    assert repo1 is repo2

def test_evaluation_repository_singleton() -> None:
    repo1 = get_evaluation_repository()
    repo2 = get_evaluation_repository()
    assert repo1 is repo2

def test_persona_repository_singleton() -> None:
    repo1 = get_persona_repository()
    repo2 = get_persona_repository()
    assert repo1 is repo2
