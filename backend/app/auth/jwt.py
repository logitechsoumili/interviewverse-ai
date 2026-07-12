"""JWT helpers for access token creation and validation."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from backend.app.core.config import settings


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT access token.

    Args:
        data: Payload data to embed in the token.
        expires_delta: Optional custom token lifetime.

    Returns:
        A signed JWT string containing the payload and ``exp`` claim.
    """
    token_data = data.copy()
    expiration = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.access_token_expire_minutes)
    )
    token_data["exp"] = expiration
    secret_key: str = settings.secret_key  # type: ignore[attr-defined]
    algorithm: str = settings.algorithm  # type: ignore[attr-defined]
    return jwt.encode(token_data, secret_key, algorithm=algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT access token.

    Args:
        token: The encoded JWT string.

    Returns:
        The decoded token payload.

    Raises:
        ExpiredSignatureError: If the token has expired.
        JWTError: If the token is invalid or the signature cannot be verified.
    """
    try:
        secret_key: str = settings.secret_key  # type: ignore[attr-defined]
        algorithm: str = settings.algorithm  # type: ignore[attr-defined]
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm],
        )
    except ExpiredSignatureError as exc:
        raise ExpiredSignatureError("Access token has expired.") from exc
    except JWTError as exc:
        raise JWTError("Unable to validate access token.") from exc

    if "exp" not in payload:
        raise JWTError("Access token is missing the exp claim.")

    return payload
