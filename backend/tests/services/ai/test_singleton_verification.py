from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from backend.app.services.ai.conversation.dependencies import get_conversation_repository
from backend.app.services.ai.interview.dependencies import get_interview_repository
from backend.app.services.ai.evaluation.dependencies import get_evaluation_repository
from backend.app.services.ai.personas.dependencies import get_persona_repository

def test_conversation_repository_behavior() -> None:
    mock_db = MagicMock(spec=Session)
    repo_with_db = get_conversation_repository(db=mock_db)
    assert repo_with_db.db is mock_db
    
    repo_without_db = get_conversation_repository(db=None)
    assert repo_without_db.db is None

def test_interview_repository_behavior() -> None:
    mock_db = MagicMock(spec=Session)
    repo_with_db = get_interview_repository(db=mock_db)
    assert repo_with_db.db is mock_db
    
    repo_without_db = get_interview_repository(db=None)
    assert repo_without_db.db is None

def test_evaluation_repository_behavior() -> None:
    mock_db = MagicMock(spec=Session)
    repo_with_db = get_evaluation_repository(db=mock_db)
    assert repo_with_db.db is mock_db
    
    repo_without_db = get_evaluation_repository(db=None)
    assert repo_without_db.db is None

def test_persona_repository_behavior() -> None:
    mock_db = MagicMock(spec=Session)
    repo_with_db = get_persona_repository(db=mock_db)
    assert repo_with_db.db is mock_db
    
    repo_without_db = get_persona_repository(db=None)
    assert repo_without_db.db is None
