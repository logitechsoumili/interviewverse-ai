from typing import List
from pydantic import BaseModel, Field

class StreamChunk(BaseModel):
    """Represents an incremental chunk of a streamed response."""
    content: str = Field(description="The incremental text content.")
    is_final: bool = Field(default=False, description="Flag indicating if this is the final chunk.")
    sequence: int = Field(ge=0, description="0-indexed sequence order of the chunk.")

class StreamResult(BaseModel):
    """Represents the final reconstructed result containing all chunks and combined text."""
    chunks: List[StreamChunk] = Field(description="Chronological list of all received stream chunks.")
    full_text: str = Field(description="Reconstructed full string response.")
