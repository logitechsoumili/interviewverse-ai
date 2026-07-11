from fastapi import Depends
from backend.app.core.config import Settings, get_settings
from backend.app.services.ai.gemini.client import GeminiClient
from backend.app.services.ai.gemini.service import GeminiService
from backend.app.services.ai.gemini.protocol import GeminiClientProtocol

def get_gemini_client(settings: Settings = Depends(get_settings)) -> GeminiClient:
    """Dependency factory to provide a configured GeminiClient instance."""
    return GeminiClient(api_key=settings.GEMINI_API_KEY)

def get_gemini_service(
    client: GeminiClientProtocol = Depends(get_gemini_client),
    settings: Settings = Depends(get_settings),
) -> GeminiService:
    """Dependency factory to provide a configured GeminiService instance.
    
    Injects the client, model, and temperature settings dynamically.
    """
    return GeminiService(
        client=client,
        model=settings.GEMINI_MODEL,
        temperature=settings.GEMINI_TEMPERATURE,
    )
