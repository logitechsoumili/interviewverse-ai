import asyncio
from typing import Any, Dict, Optional
from google.genai import types
from google.genai import errors
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
import httpx

from backend.app.core.logging import StructuredLogger
from backend.app.services.ai.gemini.protocol import GeminiClientProtocol
from backend.app.services.ai.gemini.exceptions import (
    GeminiError,
    GeminiRateLimitError,
    GeminiAuthenticationError,
    GeminiGenerationError,
)

def is_retryable_exception(exception: Exception) -> bool:
    """Determines if an exception is transient and should be retried."""
    if isinstance(exception, errors.APIError):
        # 429: Rate Limit / Resource Exhausted
        # 500, 502, 503, 504: Temporary Service Failures / Upstream failures
        if exception.code in (429, 500, 502, 503, 504):
            return True
    
    # Retry on standard networking/timeout failures
    if isinstance(exception, (httpx.TimeoutException, httpx.NetworkError, asyncio.TimeoutError)):
        return True
        
    return False

def _get_wait(retry_state) -> Any:
    """Delegates to the wait strategy configured on the service instance."""
    self = retry_state.args[0]
    return self._retry_wait(retry_state)

def _get_stop(retry_state) -> Any:
    """Delegates to the stop strategy configured on the service instance."""
    self = retry_state.args[0]
    return self._retry_stop(retry_state)


class GeminiService:
    """Service layer coordinating interaction with the Gemini API Client.
    
    Includes robust exception translation, structured logging, input validation,
    and a tenacity-based retry policy.
    """
    
    def __init__(
        self,
        client: GeminiClientProtocol,
        model: str,
        temperature: float = 0.7,
        retry_wait: Optional[Any] = None,
        retry_stop: Optional[Any] = None,
    ) -> None:
        """Initializes the service with dependency injection.
        
        Args:
            client: Gemini client conforming to GeminiClientProtocol.
            model: Model to use for generation (e.g. 'gemini-2.5-flash').
            temperature: Temperature setting for content generation (default 0.7).
            retry_wait: Optional custom tenacity wait strategy (e.g. wait_none() for testing).
            retry_stop: Optional custom tenacity stop strategy (e.g. stop_after_attempt(1)).
        """
        self.client = client
        self.model = model
        self.temperature = temperature
        self._retry_wait = retry_wait or wait_exponential(multiplier=1, min=2, max=10)
        self._retry_stop = retry_stop or stop_after_attempt(3)

    def _prepare_config(
        self,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        response_mime_type: Optional[str] = None,
        response_schema: Optional[Any] = None,
    ) -> types.GenerateContentConfig:
        """Constructs GenerateContentConfig. Designed for future extensions (schemas/mime types)."""
        config_kwargs: Dict[str, Any] = {}
        
        if system_prompt:
            config_kwargs["system_instruction"] = system_prompt
            
        config_kwargs["temperature"] = temperature if temperature is not None else self.temperature
        
        if response_mime_type:
            config_kwargs["response_mime_type"] = response_mime_type
            
        if response_schema:
            config_kwargs["response_schema"] = response_schema
            
        return types.GenerateContentConfig(**config_kwargs)

    def _prepare_contents(self, user_prompt: str) -> Any:
        """Prepares request contents. Designed to easily extend to conversation history."""
        return user_prompt

    @retry(
        stop=_get_stop,
        wait=_get_wait,
        retry=retry_if_exception(is_retryable_exception),
        reraise=True,
    )
    async def _generate_with_retry(
        self,
        contents: Any,
        config: types.GenerateContentConfig,
    ) -> str:
        """Internal call wrapped with retry logic."""
        StructuredLogger.info(
            "Sending content generation request to GeminiClient",
            extra={"model": self.model}
        )
        return await self.client.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """Generates text from the Gemini model using the system prompt and user prompt.
        
        Args:
            system_prompt: Guidelines/role for the model (system instruction).
            user_prompt: User input to respond to.
            
        Returns:
            The validated non-empty raw text response.
            
        Raises:
            GeminiRateLimitError: If rate limited.
            GeminiAuthenticationError: If auth/permissions fail.
            GeminiGenerationError: If input/model config is invalid or response is malformed.
            GeminiError: For other unexpected errors.
        """
        if not system_prompt or not system_prompt.strip():
            raise GeminiGenerationError("System prompt cannot be empty.")
        if not user_prompt or not user_prompt.strip():
            raise GeminiGenerationError("User prompt cannot be empty.")

        StructuredLogger.info(
            "Starting Gemini content generation",
            extra={"model": self.model}
        )

        config = self._prepare_config(system_prompt=system_prompt)
        contents = self._prepare_contents(user_prompt)

        try:
            response_text = await self._generate_with_retry(contents, config)
        except errors.ClientError as e:
            if e.code == 429:
                StructuredLogger.warning("Gemini API rate limit exceeded")
                raise GeminiRateLimitError("Gemini API rate limit exceeded.", original_error=e) from e
            elif e.code in (401, 403):
                StructuredLogger.error("Gemini API authentication/permission error")
                raise GeminiAuthenticationError("Gemini authentication or permission failed.", original_error=e) from e
            else:
                StructuredLogger.error(f"Gemini client API error (code {e.code})")
                raise GeminiGenerationError(f"Gemini client API error (code {e.code}): {e.message or str(e)}", original_error=e) from e
                
        except errors.ServerError as e:
            StructuredLogger.error(f"Gemini server error (code {e.code})")
            raise GeminiGenerationError(f"Gemini server error (code {e.code}): {e.message or str(e)}", original_error=e) from e
            
        except errors.APIError as e:
            StructuredLogger.error(f"Gemini generic API error (code {e.code})")
            raise GeminiError(f"Gemini API error (code {e.code}): {e.message or str(e)}", original_error=e) from e
            
        except Exception as e:
            if isinstance(e, (httpx.TimeoutException, asyncio.TimeoutError)):
                StructuredLogger.error("Gemini API request timed out")
                raise GeminiGenerationError("Gemini API request timed out.", original_error=e) from e
            if isinstance(e, httpx.NetworkError):
                StructuredLogger.error("Gemini API network error occurred")
                raise GeminiGenerationError("Gemini API network communication failed.", original_error=e) from e
                
            StructuredLogger.error(f"Unexpected error during Gemini generation: {str(e)}")
            raise GeminiError(f"Unexpected error during Gemini generation: {str(e)}", original_error=e) from e

        if response_text is None or not response_text.strip():
            StructuredLogger.error("Empty or whitespace-only response received from GeminiClient")
            raise GeminiGenerationError("Gemini response was empty or malformed.")

        StructuredLogger.info("Gemini content generation completed successfully")
        return response_text

