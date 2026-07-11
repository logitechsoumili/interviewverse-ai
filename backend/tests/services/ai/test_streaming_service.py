import pytest
from typing import Any, AsyncIterator, List, Optional
from google.genai import types
from google.genai.errors import APIError

from backend.app.services.ai.gemini.service import GeminiService
from backend.app.services.ai.gemini.exceptions import GeminiError
from backend.app.services.ai.streaming.models import StreamChunk, StreamResult
from backend.app.services.ai.streaming.service import StreamingService
from backend.app.services.ai.streaming.exceptions import (
    StreamingError,
    InvalidStreamError,
    StreamInterruptedError,
)

# ==========================================
# Mock Client and Stream Implementation
# ==========================================

class MockGeminiClient:
    """Mock Gemini client implementing generate_content_stream."""
    def __init__(self, chunks: List[str], raise_at_index: Optional[int] = None, exc_to_raise: Optional[Exception] = None) -> None:
        self.chunks = chunks
        self.raise_at_index = raise_at_index
        self.exc_to_raise = exc_to_raise

    async def generate_content(
        self,
        model: str,
        contents: Any,
        config: Optional[types.GenerateContentConfig] = None,
    ) -> str:
        return "".join(self.chunks)

    async def generate_content_stream(
        self,
        model: str,
        contents: Any,
        config: Optional[types.GenerateContentConfig] = None,
    ) -> AsyncIterator[str]:
        for idx, chunk in enumerate(self.chunks):
            if self.raise_at_index is not None and idx == self.raise_at_index:
                assert self.exc_to_raise is not None
                raise self.exc_to_raise
            yield chunk


# ==========================================
# Test Cases
# ==========================================

@pytest.mark.anyio
async def test_stream_response_success() -> None:
    """Verifies that stream_response yields sequential, validated StreamChunks."""
    chunks_data = ["hello", " ", "world", "!"]
    mock_client = MockGeminiClient(chunks=chunks_data)
    gemini_svc = GeminiService(client=mock_client, model="gemini-2.5-flash")
    streaming_svc = StreamingService(gemini_service=gemini_svc)

    chunks = []
    async for chunk in streaming_svc.stream_response(
        system_prompt="You are a helpful assistant.",
        user_prompt="Say hello."
    ):
        chunks.append(chunk)

    assert len(chunks) == 4
    # Check sequences
    assert [c.sequence for c in chunks] == [0, 1, 2, 3]
    # Check intermediate vs final flags
    assert [c.is_final for c in chunks] == [False, False, False, True]
    # Check content mapping
    assert [c.content for c in chunks] == chunks_data

@pytest.mark.anyio
async def test_collect_stream_success() -> None:
    """Verifies that collect_stream captures all chunks and reconstructs the full text."""
    chunks_data = ["gemini", " ", "streaming", " ", "is", " ", "working"]
    mock_client = MockGeminiClient(chunks=chunks_data)
    gemini_svc = GeminiService(client=mock_client, model="gemini-2.5-flash")
    streaming_svc = StreamingService(gemini_service=gemini_svc)

    result = await streaming_svc.collect_stream(
        system_prompt="System",
        user_prompt="User"
    )
    assert isinstance(result, StreamResult)
    assert len(result.chunks) == 7
    assert result.full_text == "gemini streaming is working"

def test_reconstruct_response_success() -> None:
    """Verifies reconstruction joins correct sequential chunks."""
    streaming_svc = StreamingService(gemini_service=None)  # type: ignore
    chunks = [
        StreamChunk(content="foo", sequence=0, is_final=False),
        StreamChunk(content="bar", sequence=1, is_final=True)
    ]
    reconstructed = streaming_svc.reconstruct_response(chunks)
    assert reconstructed == "foobar"

def test_reconstruct_validation_failures() -> None:
    """Verifies that reconstruct_response rejects bad ordering, empty contents, or incorrect flags."""
    streaming_svc = StreamingService(gemini_service=None)  # type: ignore

    # 1. Empty list
    with pytest.raises(InvalidStreamError) as exc:
        streaming_svc.reconstruct_response([])
    assert "No stream chunks provided" in str(exc.value)

    # 2. Out of order sequence
    bad_order = [
        StreamChunk(content="foo", sequence=0, is_final=False),
        StreamChunk(content="bar", sequence=2, is_final=True)  # skipped sequence 1
    ]
    with pytest.raises(InvalidStreamError) as exc:
        streaming_svc.reconstruct_response(bad_order)
    assert "Invalid sequence order" in str(exc.value)

    # 3. Empty chunk content
    empty_content = [
        StreamChunk(content="foo", sequence=0, is_final=False),
        StreamChunk(content="", sequence=1, is_final=True)
    ]
    with pytest.raises(InvalidStreamError) as exc:
        streaming_svc.reconstruct_response(empty_content)
    assert "has empty content" in str(exc.value)

    # 4. Final flag set early
    early_final = [
        StreamChunk(content="foo", sequence=0, is_final=True),
        StreamChunk(content="bar", sequence=1, is_final=True)
    ]
    with pytest.raises(InvalidStreamError) as exc:
        streaming_svc.reconstruct_response(early_final)
    assert "is marked final, but is not the last chunk" in str(exc.value)

    # 5. Missing final flag at the end
    missing_final = [
        StreamChunk(content="foo", sequence=0, is_final=False),
        StreamChunk(content="bar", sequence=1, is_final=False)
    ]
    with pytest.raises(InvalidStreamError) as exc:
        streaming_svc.reconstruct_response(missing_final)
    assert "must be marked final" in str(exc.value)

@pytest.mark.anyio
async def test_stream_response_validation_failures() -> None:
    """Verifies stream_response rejects empty system/user prompts or empty generators."""
    streaming_svc = StreamingService(gemini_service=None)  # type: ignore

    # Empty system prompt
    with pytest.raises(InvalidStreamError) as exc:
        async for _ in streaming_svc.stream_response("", "User"):
            pass
    assert "System prompt cannot be empty" in str(exc.value)

    # Empty user prompt
    with pytest.raises(InvalidStreamError) as exc:
        async for _ in streaming_svc.stream_response("System", "   "):
            pass
    assert "User prompt cannot be empty" in str(exc.value)

    # Empty stream output from API
    mock_client = MockGeminiClient(chunks=[])
    gemini_svc = GeminiService(client=mock_client, model="gemini-2.5-flash")
    active_svc = StreamingService(gemini_service=gemini_svc)
    with pytest.raises(InvalidStreamError) as exc:
        async for _ in active_svc.stream_response("System", "User"):
            pass
    assert "No content was generated" in str(exc.value)

@pytest.mark.anyio
async def test_stream_interrupted_error() -> None:
    """Verifies that API failures mid-stream translate to StreamInterruptedError."""
    api_error = APIError(500, {"message": "mid-stream failure"})
    mock_client = MockGeminiClient(
        chunks=["chunk0", "chunk1", "chunk2"],
        raise_at_index=2,
        exc_to_raise=api_error
    )
    # GeminiService handles APIError conversion. But if it happens during iteration,
    # generate_stream will catch it and raise GeminiError.
    gemini_svc = GeminiService(client=mock_client, model="gemini-2.5-flash")
    streaming_svc = StreamingService(gemini_service=gemini_svc)

    chunks = []
    with pytest.raises(StreamInterruptedError) as exc:
        async for chunk in streaming_svc.stream_response("System", "User"):
            chunks.append(chunk)
            
    assert len(chunks) == 1  # only first chunk yielded before index 2 exception
    assert "Stream was interrupted" in str(exc.value)
