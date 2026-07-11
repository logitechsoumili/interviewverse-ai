from typing import Any, Optional
from google import genai
from google.genai import types
from backend.app.services.ai.gemini.protocol import GeminiClientProtocol

class GeminiClient(GeminiClientProtocol):
    """Concrete implementation of GeminiClientProtocol wrapping the google-genai SDK.
    
    Acts as a thin wrapper with zero retry logic, prompt construction, or business logic.
    """
    
    def __init__(self, api_key: str) -> None:
        """Initializes the raw google-genai Client.
        
        Args:
            api_key: The Google Gemini API key.
        """
        if not api_key:
            raise ValueError("API key must be provided")
        self._client = genai.Client(api_key=api_key)

    async def generate_content(
        self,
        model: str,
        contents: Any,
        config: Optional[types.GenerateContentConfig] = None,
    ) -> str:
        """Sends an async generation request to the Gemini API and returns the raw text response.
        
        Args:
            model: The Gemini model identifier.
            contents: Prompts/messages/input contents.
            config: Optional GenerateContentConfig object.
            
        Returns:
            The raw text string response. If response has no text, returns an empty string.
        """
        response = await self._client.aio.models.generate_content(
            model=model,
            contents=contents,
            config=config,
        )
        if response.text is None:
            return ""
        return response.text

    async def aclose(self) -> None:
        """Closes the underlying asynchronous HTTP client connections."""
        await self._client.aio.aclose()
