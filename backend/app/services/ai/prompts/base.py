from typing import Literal, Optional
from pydantic import BaseModel, Field

class ConversationMessage(BaseModel):
    """Represents a single message in an interview conversation history."""
    role: Literal["interviewer", "candidate", "system"]
    content: str = Field(min_length=1, description="The content of the message.")

class PromptPayload(BaseModel):
    """Strongly typed model representing the prompt inputs sent to the LLM client."""
    system_prompt: str = Field(description="The system instruction guiding the model's persona.")
    user_prompt: str = Field(description="The formatted user prompt or content payload.")

class PromptTemplate(BaseModel):
    """Represents a structured prompt template containing system and user prompts."""
    name: str = Field(description="Unique name of the template.")
    system_template: str = Field(description="Template for the system prompt.")
    user_template: str = Field(description="Template for the user prompt.")
    version: str = Field(default="1.0.0", description="Semantic version of the template.")
    expected_output_format: str = Field(default="text", description="Expected format, e.g., 'text' or 'json'.")
