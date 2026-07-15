"""User domain service for persistence and validation."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


class DuplicateEmailError(ValueError):
    """Raised when attempting to create a user with an existing email."""


def _get_user_by_email(db: Session, email: str) -> User | None:
    """Return the user with the given email if one exists."""
    statement = select(User).where(User.email == email)
    return db.execute(statement).scalar_one_or_none()


def create_user(db: Session, user_create: UserCreate) -> User:
    """Create a user record after enforcing unique email and hashing the password.

    Args:
        db: Active SQLAlchemy session.
        user_create: Validated user creation payload.

    Returns:
        The persisted user ORM object.

    Raises:
        DuplicateEmailError: If a user already exists for the submitted email.
    """
    existing_user = _get_user_by_email(db, user_create.email)
    if existing_user is not None:
        raise DuplicateEmailError(f"User with email {user_create.email} already exists.")

    user = User(
        email=user_create.email,
        full_name=user_create.full_name,
        password_hash=hash_password(user_create.password),
    )

    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateEmailError(
            f"User with email {user_create.email} already exists."
        ) from exc

    db.refresh(user)

    db.refresh(user)

    return user



def get_user_by_email(db: Session, email: str) -> User | None:
    """Return the user with the given email if one exists."""
    return _get_user_by_email(db, email)


def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    """Return the user with the given ID if one exists."""
    statement = select(User).where(User.id == user_id)
    return db.execute(statement).scalar_one_or_none()

