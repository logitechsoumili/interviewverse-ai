from typing import Dict
from datetime import datetime, timezone
from backend.app.services.ai.interview.models import InterviewSession, InterviewStatus
from backend.app.services.ai.interview.exceptions import InterviewNotFoundError, InterviewError

class InterviewRepository:
    """In-memory repository for storing and managing InterviewSession objects."""
    
    def __init__(self) -> None:
        self._interviews: Dict[str, InterviewSession] = {}

    def create_interview(self, session: InterviewSession) -> InterviewSession:
        """Stores a new InterviewSession.
        
        Raises:
            InterviewError: If the interview session ID already exists.
        """
        if not session.interview_id or not session.interview_id.strip():
            raise InterviewError("Interview ID cannot be empty.")
        if session.interview_id in self._interviews:
            raise InterviewError(f"Interview session '{session.interview_id}' already exists.")
        self._interviews[session.interview_id] = session
        return session

    def get_interview(self, interview_id: str) -> InterviewSession:
        """Retrieves an InterviewSession by ID.
        
        Raises:
            InterviewNotFoundError: If the interview session is not found.
        """
        if not interview_id or not interview_id.strip():
            raise InterviewError("Interview ID cannot be empty.")
        if interview_id not in self._interviews:
            raise InterviewNotFoundError(f"Interview session '{interview_id}' was not found.")
        return self._interviews[interview_id]

    def update_interview(self, session: InterviewSession) -> InterviewSession:
        """Updates an existing InterviewSession.
        
        Raises:
            InterviewNotFoundError: If the interview session is not found.
        """
        if not session.interview_id or not session.interview_id.strip():
            raise InterviewError("Interview ID cannot be empty.")
        self.get_interview(session.interview_id)  # verifies existence
        self._interviews[session.interview_id] = session
        return session

    def complete_interview(self, interview_id: str) -> InterviewSession:
        """Marks an interview session as completed and sets completed_at timestamp.
        
        Raises:
            InterviewNotFoundError: If the interview session is not found.
        """
        session = self.get_interview(interview_id)
        session.status = InterviewStatus.COMPLETED
        session.completed_at = datetime.now(timezone.utc)
        self._interviews[interview_id] = session
        return session

    def delete_interview(self, interview_id: str) -> None:
        """Deletes an interview session from the repository.
        
        Raises:
            InterviewNotFoundError: If the interview session is not found.
        """
        if not interview_id or not interview_id.strip():
            raise InterviewError("Interview ID cannot be empty.")
        if interview_id not in self._interviews:
            raise InterviewNotFoundError(f"Interview session '{interview_id}' was not found.")
        del self._interviews[interview_id]
