from typing import List, Union
from backend.app.services.ai.prompts.base import PromptPayload, ConversationMessage
from backend.app.services.ai.prompts.registry import PromptRegistry
from backend.app.services.ai.prompts.renderer import PromptRenderer
from backend.app.services.ai.prompts.exceptions import PromptValidationError

class PromptBuilder:
    """Service responsible for composing and validating PromptPayloads."""
    
    def __init__(self, registry: PromptRegistry, renderer: PromptRenderer) -> None:
        """Initializes the builder with injected registry and renderer.
        
        Args:
            registry: Registry containing prompt templates.
            renderer: Renderer responsible for variable rendering and validation.
        """
        self.registry = registry
        self.renderer = renderer

    def _validate_non_empty(self, field_name: str, value: str) -> None:
        """Validates that a string value is not empty or whitespace."""
        if value is None:
            raise PromptValidationError(f"Field '{field_name}' cannot be None.")
        if not str(value).strip():
            raise PromptValidationError(f"Field '{field_name}' cannot be empty or whitespace.")

    def _format_history(self, history: List[ConversationMessage]) -> str:
        """Formats list of ConversationMessage objects into a readable chat transcript.
        
        Raises:
            PromptValidationError: If history is not a list, contains invalid messages, or is empty.
        """
        if not isinstance(history, list):
            raise PromptValidationError("Conversation history must be a list of ConversationMessage objects.")
        
        if not history:
            raise PromptValidationError("Conversation history cannot be empty.")
            
        formatted_turns = []
        for idx, msg in enumerate(history):
            if not isinstance(msg, ConversationMessage):
                raise PromptValidationError(f"Message at index {idx} is not a ConversationMessage instance.")
            self._validate_non_empty(f"history[{idx}].content", msg.content)
            
            role_name = msg.role.capitalize()
            formatted_turns.append(f"{role_name}: {msg.content.strip()}")
            
        return "\n".join(formatted_turns)

    def build_interview_prompt(
        self,
        persona_name: str,
        persona_context: str,
        topics: Union[str, List[str]],
        history: List[ConversationMessage],
        last_response: str,
    ) -> PromptPayload:
        """Builds the PromptPayload for generating an interview question.
        
        Args:
            persona_name: Name of the persona being interviewed.
            persona_context: Guidelines/information about the persona.
            topics: Focus topics (list of strings or comma-separated string).
            history: List of ConversationMessage objects.
            last_response: Candidate's last response.
            
        Returns:
            The fully rendered PromptPayload.
        """
        self._validate_non_empty("persona_name", persona_name)
        self._validate_non_empty("persona_context", persona_context)
        self._validate_non_empty("last_response", last_response)
        
        if not topics:
            raise PromptValidationError("Topics cannot be empty.")
            
        formatted_topics = ", ".join(topics) if isinstance(topics, list) else topics
        self._validate_non_empty("topics", formatted_topics)

        formatted_history = self._format_history(history)

        template = self.registry.get_template("interview_generation")

        variables = {
            "persona_name": persona_name.strip(),
            "persona_context": persona_context.strip(),
            "topics": formatted_topics.strip(),
            "history": formatted_history,
            "last_response": last_response.strip(),
        }
        return self.renderer.render(template, variables)

    def build_evaluation_prompt(
        self,
        persona_context: str,
        rubric: str,
        question: str,
        response: str,
    ) -> PromptPayload:
        """Builds the PromptPayload for generating candidate answer evaluation.
        
        Args:
            persona_context: Persona-specific context/evaluation guidelines.
            rubric: The rubric/criteria used for evaluation.
            question: The technical question asked.
            response: Candidate's response.
            
        Returns:
            The fully rendered PromptPayload.
        """
        self._validate_non_empty("persona_context", persona_context)
        self._validate_non_empty("rubric", rubric)
        self._validate_non_empty("question", question)
        self._validate_non_empty("response", response)

        template = self.registry.get_template("evaluation_generation")

        variables = {
            "persona_context": persona_context.strip(),
            "rubric": rubric.strip(),
            "question": question.strip(),
            "response": response.strip(),
        }
        return self.renderer.render(template, variables)

    def build_report_prompt(
        self,
        persona_context: str,
        evaluation_history: Union[str, List[str]],
    ) -> PromptPayload:
        """Builds the PromptPayload for generating final candidate assessment report.
        
        Args:
            persona_context: Persona-specific context/report guidelines.
            evaluation_history: List of evaluations or string representing history.
            
        Returns:
            The fully rendered PromptPayload.
        """
        self._validate_non_empty("persona_context", persona_context)
        
        if not evaluation_history:
            raise PromptValidationError("Evaluation history cannot be empty.")
            
        if isinstance(evaluation_history, list):
            for idx, ev in enumerate(evaluation_history):
                self._validate_non_empty(f"evaluation_history[{idx}]", ev)
            formatted_eval_history = "\n---\n".join(evaluation_history)
        else:
            formatted_eval_history = evaluation_history
            self._validate_non_empty("evaluation_history", formatted_eval_history)

        template = self.registry.get_template("report_generation")

        variables = {
            "persona_context": persona_context.strip(),
            "evaluation_history": formatted_eval_history.strip(),
        }
        return self.renderer.render(template, variables)
