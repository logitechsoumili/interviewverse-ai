from typing import Dict, List
from backend.app.services.ai.prompts.base import PromptTemplate
from backend.app.services.ai.prompts.exceptions import PromptTemplateNotFoundError, PromptError
from backend.app.services.ai.prompts.templates import get_default_templates

class PromptRegistry:
    """A registry for storing and retrieving PromptTemplate instances.
    
    Functions as a read-only lookup service after bootstrap is completed.
    """
    
    def __init__(self, bootstrap: bool = True) -> None:
        """Initializes the registry and optional default bootstrapping.
        
        Args:
            bootstrap: If True, automatically registers default templates and freezes registry.
        """
        self._templates: Dict[str, PromptTemplate] = {}
        self._is_bootstrapped = False
        
        if bootstrap:
            for template in get_default_templates():
                self.register_template(template)
            self._is_bootstrapped = True

    def register_template(self, template: PromptTemplate) -> None:
        """Registers a PromptTemplate.
        
        Raises:
            PromptError: If the registry is already bootstrapped / frozen.
            ValueError: If template parameters are invalid.
        """
        if self._is_bootstrapped:
            raise PromptError("Registry is bootstrapped and read-only. Cannot register new templates.")
        if not template.name or not template.name.strip():
            raise ValueError("Template name cannot be empty")
        self._templates[template.name] = template

    def get_template(self, name: str) -> PromptTemplate:
        """Retrieves a PromptTemplate by name.
        
        Raises:
            PromptTemplateNotFoundError: If the name is not registered.
        """
        if name not in self._templates:
            raise PromptTemplateNotFoundError(f"Prompt template '{name}' was not found in the registry.")
        return self._templates[name]

    def list_templates(self) -> List[str]:
        """Lists all registered template names."""
        return list(self._templates.keys())
        
    def freeze(self) -> None:
        """Freezes the registry to prevent further registrations."""
        self._is_bootstrapped = True
