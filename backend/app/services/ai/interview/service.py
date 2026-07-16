from typing import List, Optional
from datetime import datetime, timezone
from uuid import UUID
import uuid

from backend.app.services.ai.personas.service import PersonaService
from backend.app.services.ai.personas.models import PersonaType
from backend.app.services.ai.conversation.service import ConversationService
from backend.app.services.ai.prompts.builders import PromptBuilder
from backend.app.services.ai.prompts.base import ConversationMessage
from backend.app.services.ai.gemini.service import GeminiService
from backend.app.services.ai.interview.models import InterviewSession, InterviewTurnResult, InterviewStatus
from backend.app.services.ai.interview.repository import InterviewRepository
from backend.app.services.ai.interview.exceptions import (
    InterviewError,
    InterviewNotFoundError,
    InterviewAlreadyCompletedError,
    InterviewGenerationError,
)

class InterviewService:
    """Orchestrates technical interview execution using existing AI platform components with ownership boundaries."""

    def __init__(
        self,
        persona_service: PersonaService,
        conversation_service: ConversationService,
        prompt_builder: PromptBuilder,
        gemini_service: GeminiService,
        repository: InterviewRepository,
    ) -> None:
        """Initializes the service with constructor-injected dependencies."""
        self.persona_service = persona_service
        self.conversation_service = conversation_service
        self.prompt_builder = prompt_builder
        self.gemini_service = gemini_service
        self.repository = repository

    def _validate_non_empty(self, field_name: str, value: str) -> None:
        """Helper to reject empty or whitespace strings."""
        if not value or not value.strip():
            raise InterviewError(f"{field_name} cannot be empty or whitespace.")

    async def _generate_unique_question(
        self,
        interview_id: str,
        persona_name: str,
        persona_context: str,
        topics: List[str],
        history: List[ConversationMessage],
        last_response: str,
    ) -> str:
        """Generates a follow-up question using Gemini and retries to avoid duplicates.
        
        Attempts generation up to 4 times (1 initial + 3 retries) and checks uniqueness using
        the ConversationService.
        
        Raises:
            InterviewGenerationError: If a unique question cannot be generated.
        """
        max_retries = 3
        attempts = 0
        
        while attempts <= max_retries:
            prompt_payload = self.prompt_builder.build_interview_prompt(
                persona_name=persona_name,
                persona_context=persona_context,
                topics=topics,
                history=history,
                last_response=last_response
            )
            
            question = await self.gemini_service.generate(
                system_prompt=prompt_payload.system_prompt,
                user_prompt=prompt_payload.user_prompt
            )
            
            # Check for duplicate questions in the conversation session
            if not self.conversation_service.has_similar_question(interview_id, question):
                return question
                
            attempts += 1
            
        raise InterviewGenerationError(
            f"Failed to generate a unique question after {max_retries + 1} attempts."
        )

    async def start_interview(
        self,
        interview_id: str,
        persona_id: PersonaType | str,
        topics: List[str],
        difficulty: str,
        user_id: Optional[UUID] = None,
    ) -> InterviewTurnResult:
        """Validates the persona, creates sessions, generates the opening question, and stores it with ownership.
        
        Args:
            interview_id: Unique identifier for this interview session.
            persona_id: Target interviewer persona ID.
            topics: Focus topics.
            difficulty: Interview difficulty level.
            user_id: Optional owner user ID.
            
        Returns:
            The InterviewTurnResult containing the opening question.
            
        Raises:
            InterviewError: For empty parameter values or validation errors.
            InterviewGenerationError: If the opening question generation fails.
        """
        self._validate_non_empty("Interview ID", interview_id)
        self._validate_non_empty("Difficulty", difficulty)
        if not topics:
            raise InterviewError("Topics list cannot be empty.")
        for idx, topic in enumerate(topics):
            self._validate_non_empty(f"Topic[{idx}]", topic)
            
        if not user_id:
            user_id = uuid.UUID("00000000-0000-0000-0000-000000000000")

        # 1. Validate persona and get context under user ownership boundaries
        self.persona_service.get_persona(persona_id.value if hasattr(persona_id, 'value') else str(persona_id), user_id=user_id)
        persona_context_obj = self.persona_service.get_prompt_context(persona_id.value if hasattr(persona_id, 'value') else str(persona_id), user_id=user_id)

        # 2. Create conversation session
        self.conversation_service.create_session(session_id=interview_id, persona_id=persona_id)

        # 3. Create interview session
        session = InterviewSession(
            interview_id=interview_id,
            session_id=interview_id,
            persona_id=persona_id,
            user_id=user_id,
            status=InterviewStatus.IN_PROGRESS,
            topics=topics,
            difficulty=difficulty,
            created_at=datetime.now(timezone.utc)
        )
        self.repository.create_interview(session)

        # 4. Generate opening question
        history = [
            ConversationMessage(role="system", content="[System: Initiate the technical interview.]")
        ]
        last_response = "[System: Candidate has joined and is ready.]"
        
        opening_question = await self._generate_unique_question(
            interview_id=interview_id,
            persona_name=persona_context_obj.persona_name,
            persona_context=persona_context_obj.persona_context,
            topics=topics,
            history=history,
            last_response=last_response
        )

        # 5. Store opening question
        self.conversation_service.append_interviewer_turn(interview_id, opening_question)

        # 6. Return InterviewTurnResult
        turn_count = self.conversation_service.get_turn_count(interview_id)
        return InterviewTurnResult(
            question=opening_question,
            is_final=False,
            turn_count=turn_count
        )

    async def process_response(
        self,
        interview_id: str,
        candidate_response: str,
        user_id: Optional[UUID] = None,
    ) -> InterviewTurnResult:
        """Stores candidate response, builds prompt, and generates a unique follow-up question.
        
        Args:
            interview_id: Unique identifier for the interview session.
            candidate_response: Candidate response string.
            user_id: Optional owner user ID.
            
        Returns:
            The InterviewTurnResult containing the follow-up question.
            
        Raises:
            InterviewNotFoundError: If session doesn't exist.
            InterviewAlreadyCompletedError: If the interview session is already completed.
            InterviewGenerationError: If unique question generation fails.
        """
        self._validate_non_empty("Interview ID", interview_id)
        self._validate_non_empty("Candidate response", candidate_response)

        # 1. Verify session exists, is active, and belongs to user
        session = self.repository.get_interview(interview_id, user_id=user_id)
        if session.status == InterviewStatus.COMPLETED:
            raise InterviewAlreadyCompletedError("Cannot process response for a completed interview.")

        # 2. Store candidate response
        self.conversation_service.append_candidate_turn(interview_id, candidate_response)

        # 3. Build conversation history
        history = self.conversation_service.build_llm_ready_history(interview_id)

        # 4. Generate follow-up question
        persona_context_obj = self.persona_service.get_prompt_context(
            session.persona_id.value if hasattr(session.persona_id, 'value') else str(session.persona_id),
            user_id=user_id
        )
        
        follow_up_question = await self._generate_unique_question(
            interview_id=interview_id,
            persona_name=persona_context_obj.persona_name,
            persona_context=persona_context_obj.persona_context,
            topics=session.topics,
            history=history,
            last_response=candidate_response
        )

        # 5. Store generated question
        self.conversation_service.append_interviewer_turn(interview_id, follow_up_question)

        # 6. Return InterviewTurnResult
        turn_count = self.conversation_service.get_turn_count(interview_id)
        return InterviewTurnResult(
            question=follow_up_question,
            is_final=False,
            turn_count=turn_count
        )

    def complete_interview(self, interview_id: str, user_id: Optional[UUID] = None) -> InterviewTurnResult:
        """Marks the interview as completed and deactivates the conversation session.
        
        Args:
            interview_id: Unique identifier for the interview session.
            user_id: Optional owner user ID.
            
        Returns:
            InterviewTurnResult with is_final=True.
            
        Raises:
            InterviewNotFoundError: If session doesn't exist.
            InterviewAlreadyCompletedError: If the interview session is already completed.
        """
        self._validate_non_empty("Interview ID", interview_id)

        # Verify existence, ownership, and completed status
        session = self.repository.get_interview(interview_id, user_id=user_id)
        if session.status == InterviewStatus.COMPLETED:
            raise InterviewAlreadyCompletedError("Interview is already completed.")

        # 1. Update interview session status in repository
        self.repository.complete_interview(interview_id, user_id=user_id)

        # 2. Deactivate conversation session
        conv_session = self.conversation_service.repository.get_session(interview_id)
        conv_session.is_active = False

        # 3. Return final result
        turn_count = self.conversation_service.get_turn_count(interview_id)
        return InterviewTurnResult(
            question="The interview is completed. Thank you!",
            is_final=True,
            turn_count=turn_count
        )

    def get_interview(self, interview_id: str, user_id: Optional[UUID] = None) -> InterviewSession:
        """Retrieves an existing InterviewSession by ID, enforcing user ownership."""
        self._validate_non_empty("Interview ID", interview_id)
        return self.repository.get_interview(interview_id, user_id=user_id)

    def list_interviews(self, user_id: UUID) -> List[InterviewSession]:
        """Lists all interview sessions for the specified user."""
        return self.repository.list_interviews(user_id=user_id)
