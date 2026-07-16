"""User request and response schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    """Payload for creating a new user."""

    email: EmailStr
    full_name: str
    password: str


class UserResponse(BaseModel):
    """Public user representation returned by the API."""

    id: UUID
    email: EmailStr
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Payload for authenticating a user."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Access token response representation."""

    access_token: str
    token_type: str = "bearer"

