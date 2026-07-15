import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock
from google.genai import errors
from google.genai import types
from tenacity import wait_none, stop_after_attempt
import httpx

from backend.app.services.ai.gemini.service import GeminiService
from backend.app.services.ai.gemini.protocol import GeminiClientProtocol
from backend.app.services.ai.gemini.exceptions import (
    GeminiError,
    GeminiRateLimitError,
    GeminiAuthenticationError,
    GeminiGenerationError,
)

@pytest.fixture
def mock_client() -> MagicMock:
    """Fixture to provide a mocked GeminiClientProtocol."""
    client = MagicMock(spec=GeminiClientProtocol)
    client.generate_content = AsyncMock()
    return client

@pytest.fixture
def service(mock_client: MagicMock) -> GeminiService:
    """Fixture to provide GeminiService configured for instant execution during tests."""
    return GeminiService(
        client=mock_client,
        model="gemini-2.5-flash",
        temperature=0.7,
        retry_wait=wait_none(),
        retry_stop=stop_after_attempt(3),
    )

@pytest.mark.asyncio
async def test_generate_success(service: GeminiService, mock_client: MagicMock) -> None:
    """Verifies successful generation returns correct text and parameters are passed properly."""
    mock_client.generate_content.return_value = "Mocked Response Text"

    response = await service.generate(system_prompt="System Prompt", user_prompt="User Prompt")

    assert response == "Mocked Response Text"
    mock_client.generate_content.assert_called_once()
    args, kwargs = mock_client.generate_content.call_args
    assert kwargs["model"] == "gemini-2.5-flash"
    assert kwargs["contents"] == "User Prompt"
    assert kwargs["config"].system_instruction == "System Prompt"
    assert kwargs["config"].temperature == 0.7

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "system_p, user_p",
    [
        ("", "User"),
        ("System", ""),
        ("   ", "User"),
        ("System", "   "),
        (None, "User"),
        ("System", None),
    ]
)
async def test_generate_input_validation(service: GeminiService, system_p: str, user_p: str) -> None:
    """Verifies that empty or whitespace prompts raise GeminiGenerationError."""
    with pytest.raises(GeminiGenerationError) as exc_info:
        await service.generate(system_prompt=system_p, user_prompt=user_p)
    assert "cannot be empty" in str(exc_info.value)

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "empty_response",
    [
        "",
        "   ",
        None,
    ]
)
async def test_generate_response_validation(service: GeminiService, mock_client: MagicMock, empty_response: str) -> None:
    """Verifies that empty or whitespace client responses raise GeminiGenerationError."""
    mock_client.generate_content.return_value = empty_response

    with pytest.raises(GeminiGenerationError) as exc_info:
        await service.generate(system_prompt="System", user_prompt="User")
    assert "response was empty or malformed" in str(exc_info.value)

@pytest.mark.asyncio
async def test_generate_retry_success(service: GeminiService, mock_client: MagicMock) -> None:
    """Verifies that a transient rate limit error (429) is retried and succeeds on the second attempt."""
    rate_limit_error = errors.ClientError(
        code=429,
        response_json={"error": {"message": "Quota exceeded", "status": "RESOURCE_EXHAUSTED"}}
    )
    mock_client.generate_content.side_effect = [
        rate_limit_error,
        "Success Response Text"
    ]

    response = await service.generate(system_prompt="System", user_prompt="User")

    assert response == "Success Response Text"
    assert mock_client.generate_content.call_count == 2

@pytest.mark.asyncio
async def test_generate_retry_exhaustion_rate_limit(service: GeminiService, mock_client: MagicMock) -> None:
    """Verifies that rate limit error retries up to 3 attempts and raises GeminiRateLimitError when exhausted."""
    rate_limit_error = errors.ClientError(
        code=429,
        response_json={"error": {"message": "Quota exceeded", "status": "RESOURCE_EXHAUSTED"}}
    )
    mock_client.generate_content.side_effect = [
        rate_limit_error,
        rate_limit_error,
        rate_limit_error,
    ]

    with pytest.raises(GeminiRateLimitError) as exc_info:
        await service.generate(system_prompt="System", user_prompt="User")
    
    assert mock_client.generate_content.call_count == 3
    assert "rate limit exceeded" in str(exc_info.value)
    assert exc_info.value.original_error == rate_limit_error

@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [401, 403])
async def test_generate_no_retry_auth_error(service: GeminiService, mock_client: MagicMock, status_code: int) -> None:
    """Verifies that authentication errors (401, 403) fail immediately without retrying."""
    auth_error = errors.ClientError(
        code=status_code,
        response_json={"error": {"message": "Auth failure", "status": "UNAUTHENTICATED"}}
    )
    mock_client.generate_content.side_effect = auth_error

    with pytest.raises(GeminiAuthenticationError) as exc_info:
        await service.generate(system_prompt="System", user_prompt="User")
        
    assert mock_client.generate_content.call_count == 1
    assert "authentication or permission failed" in str(exc_info.value)
    assert exc_info.value.original_error == auth_error

@pytest.mark.asyncio
async def test_generate_no_retry_invalid_request(service: GeminiService, mock_client: MagicMock) -> None:
    """Verifies that request errors like bad inputs (400) fail immediately without retrying."""
    invalid_arg_error = errors.ClientError(
        code=400,
        response_json={"error": {"message": "Invalid model argument", "status": "INVALID_ARGUMENT"}}
    )
    mock_client.generate_content.side_effect = invalid_arg_error

    with pytest.raises(GeminiGenerationError) as exc_info:
        await service.generate(system_prompt="System", user_prompt="User")
        
    assert mock_client.generate_content.call_count == 1
    assert "Gemini client API error" in str(exc_info.value)
    assert exc_info.value.original_error == invalid_arg_error

@pytest.mark.asyncio
async def test_generate_retry_and_exhaustion_server_error(service: GeminiService, mock_client: MagicMock) -> None:
    """Verifies that server errors (500) are retried and map to GeminiGenerationError on exhaustion."""
    server_error = errors.ServerError(
        code=500,
        response_json={"error": {"message": "Internal error", "status": "INTERNAL"}}
    )
    mock_client.generate_content.side_effect = [
        server_error,
        server_error,
        server_error,
    ]

    with pytest.raises(GeminiGenerationError) as exc_info:
        await service.generate(system_prompt="System", user_prompt="User")

    assert mock_client.generate_content.call_count == 3
    assert "Gemini server error" in str(exc_info.value)
    assert exc_info.value.original_error == server_error

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "network_error_instance",
    [
        httpx.TimeoutException("Timeout"),
        httpx.NetworkError("Network issue"),
        asyncio.TimeoutError(),
    ]
)
async def test_generate_retry_network_and_timeout_errors(
    service: GeminiService,
    mock_client: MagicMock,
    network_error_instance: Exception
) -> None:
    """Verifies that network issues and timeouts trigger retries and map to GeminiGenerationError on exhaustion."""
    mock_client.generate_content.side_effect = [
        network_error_instance,
        network_error_instance,
        network_error_instance,
    ]

    with pytest.raises(GeminiGenerationError) as exc_info:
        await service.generate(system_prompt="System", user_prompt="User")
        
    assert mock_client.generate_content.call_count == 3
    assert "timed out" in str(exc_info.value) or "network communication failed" in str(exc_info.value)
    assert exc_info.value.original_error == network_error_instance

@pytest.mark.asyncio
async def test_generate_unexpected_error_no_retry(service: GeminiService, mock_client: MagicMock) -> None:
    """Verifies that unexpected errors (e.g. ValueError) are not retried and map to GeminiError."""
    unexpected = ValueError("Unexpected system failure")
    mock_client.generate_content.side_effect = unexpected

    with pytest.raises(GeminiError) as exc_info:
        await service.generate(system_prompt="System", user_prompt="User")
        
    assert mock_client.generate_content.call_count == 1
    assert "Unexpected error during Gemini generation" in str(exc_info.value)
    assert exc_info.value.original_error == unexpected
