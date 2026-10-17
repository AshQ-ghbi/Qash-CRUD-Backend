"""Application settings (backend: app/config.py)."""
import os


class Settings:
    """Central configuration. Values can be overridden via environment variables."""

    APP_NAME: str = "EWB Edu Tech Students Database API"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./students.db")

    # Used in Phase 3 (optional Ollama integration)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:1b")


settings = Settings()
