import re
from typing import Any, Dict, Set
from backend.app.services.ai.prompts.base import PromptTemplate, PromptPayload
from backend.app.services.ai.prompts.exceptions import PromptValidationError

class PromptRenderer:
    """Abstraction responsible for rendering templates and validating placeholders."""
    
    @staticmethod
    def _extract_placeholders(template_str: str) -> Set[str]:
        """Finds all placeholder keys matching {placeholder_name} in the string."""
        return set(re.findall(r'(?<!{){([a-zA-Z0-9_]+)}(?!})', template_str))

    def render(self, template: PromptTemplate, variables: Dict[str, Any]) -> PromptPayload:
        """Renders the PromptTemplate with the provided variables.
        
        Validates that all placeholders in the template are successfully rendered.
        
        Args:
            template: The PromptTemplate to render.
            variables: Key-value dictionary containing template substitutions.
            
        Returns:
            A PromptPayload containing the fully rendered prompts.
            
        Raises:
            PromptValidationError: If required variables are missing, are None, or if placeholders
                                   remain unrendered.
        """
        sys_placeholders = self._extract_placeholders(template.system_template)
        user_placeholders = self._extract_placeholders(template.user_template)
        all_required = sys_placeholders.union(user_placeholders)

        # Validate that all required placeholder keys exist in variables
        missing_keys = all_required - set(variables.keys())
        if missing_keys:
            raise PromptValidationError(
                f"Missing template variables required for rendering: {', '.join(missing_keys)}"
            )

        # Validate that no variable values are None or empty
        for key in all_required:
            val = variables.get(key)
            if val is None:
                raise PromptValidationError(f"Variable '{key}' cannot be None.")
            if isinstance(val, str) and not val.strip():
                raise PromptValidationError(f"Variable '{key}' cannot be empty or whitespace-only.")

        try:
            system_prompt = template.system_template.format(**variables)
            user_prompt = template.user_template.format(**variables)
        except Exception as e:
            raise PromptValidationError(f"Failed to render prompt template '{template.name}': {str(e)}") from e

        # Verify no residual placeholders remain in the output
        residual_sys = self._extract_placeholders(system_prompt)
        residual_user = self._extract_placeholders(user_prompt)
        if residual_sys or residual_user:
            all_residuals = residual_sys.union(residual_user)
            raise PromptValidationError(
                f"Prompt contains unrendered residual placeholders: {', '.join(all_residuals)}"
            )

        return PromptPayload(system_prompt=system_prompt, user_prompt=user_prompt)
