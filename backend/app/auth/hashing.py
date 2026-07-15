"""Password hashing utilities."""

from __future__ import annotations

import bcrypt


def hash_password(password: str) -> str:
    """Hash a plain-text password with bcrypt.

    Args:
        password: The plain-text password to hash.

    Returns:
        A bcrypt password hash as a string.
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored hash.

    Args:
        plain_password: The candidate password to verify.
        hashed_password: The stored bcrypt hash.

    Returns:
        True when the password matches the hash, otherwise False.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False

