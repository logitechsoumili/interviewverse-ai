from typing import Any, AsyncIterator, Optional, Protocol
from google.genai import types

class GeminiClientProtocol(Protocol):
    """Protocol defining the interface for the Gemini API Client.
    
    This decouples the GeminiService from the concrete SDK client implementation.
    """
    
    async def generate_content(
        self,
        model: str,
        contents: Any,
        config: Optional[types.GenerateContentConfig] = None,
    ) -> str:
        """Sends an asynchronous generation request to the Gemini API and returns raw text.
        
        Args:
            model: The name of the Gemini model to use.
            contents: The prompts or multi-turn content for generation.
            config: Optional GenerateContentConfig object.
            
        Returns:
            The raw string response returned by the Gemini API.
        """
        ...

    async def generate_content_stream(
        self,
        model: str,
        contents: Any,
        config: Optional[types.GenerateContentConfig] = None,
    ) -> AsyncIterator[str]:
        """Sends an asynchronous streaming generation request to the Gemini API and yields raw text chunks.
        
        Args:
            model: The name of the Gemini model to use.
            contents: The prompts or multi-turn content for generation.
            config: Optional GenerateContentConfig object.
            
        Yields:
            Incremental text chunks.
        """
        ...

