import os
# pyrefly: ignore [missing-import]
import pytest
from datetime import timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.auth.jwt import create_access_token
# Import models using the 'app' package prefix to avoid duplicate imports
from app.models import user, interview_session, message, report, persona

# Setup file-based SQLite for testing to support concurrent thread access
DB_FILE = "test.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    # Clean up previous test database if it exists
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
        except PermissionError:
            pass

    # Create tables in the test DB
    Base.metadata.create_all(bind=engine)
    # Register dependency override
    app.dependency_overrides[get_db] = override_get_db
    yield
    # Clean up overrides
    app.dependency_overrides.clear()
    
    # Close connection pool to release file locks
    engine.dispose()
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
        except PermissionError:
            pass


client = TestClient(app)


def test_register_and_login_flow() -> None:
    # 1. Register a new user
    user_payload = {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "securepassword123",
    }
    response = client.post("/api/v1/auth/register", json=user_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_payload["email"]
    assert data["full_name"] == user_payload["full_name"]
    assert "id" in data
    assert "created_at" in data

    # 2. Attempt duplicate registration -> HTTP 409
    response_dup = client.post("/api/v1/auth/register", json=user_payload)
    assert response_dup.status_code == 409
    assert response_dup.json()["detail"] == "Email already exists."

    # 3. Login with correct credentials -> get JWT token
    login_payload = {
        "username": user_payload["email"],
        "password": user_payload["password"],
    }
    response_login = client.post("/api/v1/auth/login", data=login_payload)
    assert response_login.status_code == 200
    login_data = response_login.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"

    # 4. Call protected route /users/me using retrieved token
    token = login_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response_me = client.get("/api/v1/users/me", headers=headers)
    assert response_me.status_code == 200
    me_data = response_me.json()
    assert me_data["email"] == user_payload["email"]
    assert me_data["full_name"] == user_payload["full_name"]
    assert me_data["id"] == data["id"]


def test_login_invalid_credentials() -> None:
    # Attempt to login a user that doesn't exist
    login_payload = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword",
    }
    response = client.post("/api/v1/auth/login", data=login_payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password."

    # Register user
    user_payload = {
        "email": "anotheruser@example.com",
        "full_name": "Another User",
        "password": "securepassword123",
    }
    client.post("/api/v1/auth/register", json=user_payload)

    # Login with incorrect password
    login_payload_wrong_pw = {
        "username": user_payload["email"],
        "password": "wrongpassword",
    }
    response_wrong_pw = client.post("/api/v1/auth/login", data=login_payload_wrong_pw)
    assert response_wrong_pw.status_code == 401
    assert response_wrong_pw.json()["detail"] == "Incorrect email or password."


def test_protected_route_negative_scenarios() -> None:
    # 1. Missing Token
    response_missing = client.get("/api/v1/users/me")
    assert response_missing.status_code == 401
    assert response_missing.json()["detail"] == "Not authenticated"

    # 2. Invalid Token
    headers_invalid = {"Authorization": "Bearer invalidtokenvalue123"}
    response_invalid = client.get("/api/v1/users/me", headers=headers_invalid)
    assert response_invalid.status_code == 401
    assert response_invalid.json()["detail"] == "Could not validate credentials."

    # 3. Expired Token
    # Create an access token that is already expired
    expired_token = create_access_token(
        data={"sub": "00000000-0000-0000-0000-000000000000"},
        expires_delta=timedelta(minutes=-30),
    )
    headers_expired = {"Authorization": f"Bearer {expired_token}"}
    response_expired = client.get("/api/v1/users/me", headers=headers_expired)
    assert response_expired.status_code == 401
    assert response_expired.json()["detail"] == "Access token has expired."
