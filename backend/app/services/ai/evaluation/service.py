import json
import re
from datetime import datetime, timezone
from typing import List, Optional

from backend.app.core.logging import StructuredLogger
from backend.app.services.ai.personas.service import PersonaService
from backend.app.services.ai.personas.models import PersonaType
from backend.app.services.ai.conversation.service import ConversationService
from backend.app.services.ai.prompts.builders import PromptBuilder
from backend.app.services.ai.gemini.service import GeminiService
from backend.app.services.ai.interview.service import InterviewService
from backend.app.services.ai.interview.models import InterviewStatus
from backend.app.services.ai.evaluation.models import EvaluationResult
from backend.app.services.ai.evaluation.exceptions import (
    EvaluationError,
    EvaluationParsingError,
    InvalidEvaluationError,
)

class EvaluationService:
    """Evaluation Engine Service responsible for generating structured interview evaluations."""

    def __init__(
        self,
        prompt_builder: PromptBuilder,
        gemini_service: GeminiService,
        conversation_service: ConversationService,
        persona_service: PersonaService,
        interview_service: InterviewService,
    ) -> None:
        """Initializes the service with constructor-injected dependencies.
        
        Args:
            prompt_builder: Injected PromptBuilder.
            gemini_service: Injected GeminiService.
            conversation_service: Injected ConversationService.
            persona_service: Injected PersonaService.
            interview_service: Injected InterviewService.
        """
        self.prompt_builder = prompt_builder
        self.gemini_service = gemini_service
        self.conversation_service = conversation_service
        self.persona_service = persona_service
        self.interview_service = interview_service

    def _validate_non_empty(self, field_name: str, value: str) -> None:
        """Helper to reject empty or whitespace strings."""
        if not value or not value.strip():
            raise InvalidEvaluationError(f"{field_name} cannot be empty or whitespace.")

    def _extract_json_payload(self, raw_response: str) -> str:
        """Robustly extracts the first JSON object payload from raw text.
        
        Handles markdown fences, surrounding explanatory text, whitespace variations, etc.
        
        Args:
            raw_response: The raw response text from the LLM.
            
        Returns:
            The extracted JSON substring.
            
        Raises:
            EvaluationParsingError: If no JSON object can be extracted.
        """
        if not raw_response or not raw_response.strip():
            raise EvaluationParsingError("Raw response is empty or whitespace-only.")

        cleaned = raw_response.strip()

        # 1. Attempt to match a markdown code block if present
        markdown_match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.DOTALL | re.IGNORECASE)
        if markdown_match:
            candidate = markdown_match.group(1).strip()
            # If candidate starts with { and ends with }, we can return it directly
            if candidate.startswith("{") and candidate.endswith("}"):
                return candidate
            # Otherwise fall back to brace searching in the matched block
            cleaned = candidate

        # 2. Find the first '{' and the last '}' to extract surrounding text
        start_idx = cleaned.find("{")
        end_idx = cleaned.rfind("}")

        if start_idx == -1 or end_idx == -1 or start_idx > end_idx:
            raise EvaluationParsingError("Could not find a valid JSON object structure in the response.")

        return cleaned[start_idx : end_idx + 1].strip()

    def parse_evaluation_response(
        self,
        raw_response: str,
        persona_id: PersonaType,
        evaluated_at: Optional[datetime] = None,
    ) -> EvaluationResult:
        """Parses the raw JSON response from Gemini, handles cleaning, and validates schema.
        
        Args:
            raw_response: Raw content string returned by Gemini.
            persona_id: Persona ID of the interviewer who conducted the session.
            evaluated_at: Optional timestamp of when evaluation occurred. Defaults to current UTC time.
            
        Returns:
            The parsed and validated EvaluationResult.
            
        Raises:
            EvaluationParsingError: If json is malformed or invalid json.
            InvalidEvaluationError: If validation rules fail (missing fields, invalid scores).
        """
        if evaluated_at is None:
            evaluated_at = datetime.now(timezone.utc)

        # Extract only the JSON payload portion
        json_payload = self._extract_json_payload(raw_response)

        try:
            data = json.loads(json_payload)
        except json.JSONDecodeError as e:
            StructuredLogger.error(f"Failed to decode evaluation JSON: {str(e)}", extra={"json_payload": json_payload})
            raise EvaluationParsingError(f"Failed to parse LLM response as JSON: {str(e)}") from e

        if not isinstance(data, dict):
            raise InvalidEvaluationError("Decoded JSON is not a dictionary.")

        # Inject metadata fields required by EvaluationResult model
        data["evaluated_at"] = evaluated_at
        data["persona_id"] = persona_id

        try:
            return EvaluationResult(**data)
        except Exception as e:
            log_data = {}
            for k, v in data.items():
                if isinstance(v, datetime):
                    log_data[k] = v.isoformat()
                elif isinstance(v, PersonaType):
                    log_data[k] = v.value
                else:
                    log_data[k] = v
            StructuredLogger.error(f"Failed to validate evaluation result schema: {str(e)}", extra={"data": log_data})
            raise InvalidEvaluationError(f"Validation failed for evaluation result schema: {str(e)}") from e

    async def evaluate_interview(self, interview_id: str) -> EvaluationResult:
        """Orchestrates the evaluation of a completed interview session.
        
        Args:
            interview_id: Unique identifier for the interview session.
            
        Returns:
            The generated and validated EvaluationResult.
            
        Raises:
            InvalidEvaluationError: For empty histories, status not COMPLETED, or parameter validation errors.
            EvaluationParsingError: If LLM response cannot be parsed.
            EvaluationError: For general execution failures.
        """
        self._validate_non_empty("Interview ID", interview_id)

        # 1. Retrieve the interview session
        try:
            session = self.interview_service.repository.get_interview(interview_id)
        except Exception as e:
            raise InvalidEvaluationError(f"Interview session '{interview_id}' was not found.") from e

        # 2. Validate that the interview status is COMPLETED before evaluation
        if session.status != InterviewStatus.COMPLETED:
            raise InvalidEvaluationError(
                f"Cannot evaluate interview '{interview_id}' in state '{session.status.value}'. "
                f"Status must be '{InterviewStatus.COMPLETED.value}'."
            )

        # 3. Retrieve history from ConversationService
        try:
            history = self.conversation_service.build_llm_ready_history(interview_id)
        except Exception as e:
            raise InvalidEvaluationError(f"Failed to retrieve conversation history: {str(e)}") from e

        # Reject empty history
        if not history:
            raise InvalidEvaluationError("Cannot evaluate interview with an empty conversation history.")

        StructuredLogger.info(
            "Starting interview evaluation orchestration",
            extra={"interview_id": interview_id}
        )

        # 4. Retrieve persona context using PersonaService
        try:
            persona_prompt_context = self.persona_service.get_prompt_context(session.persona_id)
        except Exception as e:
            raise EvaluationError(f"Failed to retrieve persona context: {str(e)}") from e

        # 5. Build evaluation prompt
        try:
            prompt_payload = self.prompt_builder.build_interview_evaluation_prompt(
                persona_context=persona_prompt_context.persona_context,
                history=history,
            )
        except Exception as e:
            raise EvaluationError(f"Failed to build evaluation prompt: {str(e)}") from e

        # 6. Call Gemini (use deterministic settings: temperature=0.0)
        try:
            raw_response = await self.gemini_service.generate(
                system_prompt=prompt_payload.system_prompt,
                user_prompt=prompt_payload.user_prompt,
                temperature=0.0,
            )
        except Exception as e:
            StructuredLogger.error(f"Gemini generation failed for interview {interview_id}: {str(e)}")
            raise EvaluationError(f"Gemini evaluation generation failed: {str(e)}") from e

        # 7. Parse response & return EvaluationResult
        return self.parse_evaluation_response(raw_response, persona_id=session.persona_id)
