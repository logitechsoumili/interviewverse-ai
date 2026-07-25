"""Application settings loaded from environment variables."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BACKEND_DIR / ".env"

load_dotenv(ENV_FILE, override=True)


class Settings(BaseSettings):
    """Runtime configuration for InterviewVerse AI."""

    app_name: str = Field(default="InterviewVerse AI", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")

    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/interviewverse",
        alias="DATABASE_URL",
    )

    allowed_origins: list[str] = Field(
        default=["http://localhost:3000"],
        alias="ALLOWED_ORIGINS",
    )

    SECRET_KEY: str = Field(..., alias="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    # Gemini configuration fields from HEAD
    GEMINI_API_KEY: str = Field(..., alias="GEMINI_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-2.5-flash", alias="GEMINI_MODEL")
    GEMINI_TEMPERATURE: float = Field(default=0.7, alias="GEMINI_TEMPERATURE")

    @field_validator("database_url", mode="before")
    @classmethod
    def assemble_db_url(cls, v: str) -> str:
        if isinstance(v, str):
            if v.startswith("postgres://"):
                return v.replace("postgres://", "postgresql+psycopg://", 1)
            elif v.startswith("postgresql://"):
                return v.replace("postgresql://", "postgresql+psycopg://", 1)
        return v

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            v_stripped = v.strip()
            if v_stripped.startswith("[") and v_stripped.endswith("]"):
                import json
                try:
                    return json.loads(v_stripped)
                except Exception:
                    pass
            return [origin.strip() for origin in v_stripped.split(",") if origin.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
        extra="ignore"
    )

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
