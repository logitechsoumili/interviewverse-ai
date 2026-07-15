
"""Authentication routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.auth.hashing import verify_password
from app.auth.jwt import create_access_token
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.user_service import DuplicateEmailError, create_user, get_user_by_email

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_create: UserCreate,
    db: Annotated[Session, Depends(get_db)],
) -> UserResponse:
    """Register a new user account."""
    try:
        user = create_user(db, user_create)
    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        ) from exc

    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    """Authenticate a user using standard credentials and return a JWT access token."""
    user = get_user_by_email(db, form_data.username)
    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")

