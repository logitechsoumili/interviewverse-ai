"""Password hashing utilities."""

from __future__ import annotations

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password with bcrypt.

    Args:
        password: The plain-text password to hash.

    Returns:
        A bcrypt password hash.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored hash.

    Args:
        plain_password: The candidate password to verify.
        hashed_password: The stored bcrypt hash.

    Returns:
        True when the password matches the hash, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)
