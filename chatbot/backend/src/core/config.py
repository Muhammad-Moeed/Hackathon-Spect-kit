"""
Configuration module for the Book RAG System
Handles environment variables and application settings
"""
import os
from pathlib import Path
from typing import List, Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings


# Get the backend directory (parent of src)
BACKEND_DIR = Path(__file__).parent.parent.parent
ENV_FILE = BACKEND_DIR / ".env"


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API settings
    API_TITLE: str = "Book RAG System API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database settings
    NEON_POSTGRES_URL: str = ""

    # Vector store settings
    QDRANT_URL: str = ""
    QDRANT_API_KEY: str = ""

    # OpenAI settings (optional if using free embeddings)
    OPENAI_API_KEY: str = ""

    # Cohere settings (optional - free tier available)
    COHERE_API_KEY: str = ""

    # Embedding settings
    EMBEDDING_TYPE: str = "cohere"  # Options: "cohere" (default), "openai", or "sentence-transformers"
    EMBEDDING_MODEL_NAME: str = "embed-english-v3.0"  # Model name (Cohere: embed-english-v3.0, sentence-transformers: all-MiniLM-L6-v2)

    # Application settings
    MAX_CONCURRENT_USERS: int = 100
    RESPONSE_TIMEOUT: float = 3.0  # seconds
    RETRIEVAL_TIMEOUT: float = 1.5  # seconds

    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]  # In production, specify exact origins

    # Chunking settings
    DEFAULT_CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50

    class Config:
        env_file = str(ENV_FILE) if ENV_FILE.exists() else ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


def validate_settings():
    """Validate that all required settings are present"""
    errors = []

    if not settings.NEON_POSTGRES_URL:
        errors.append("NEON_POSTGRES_URL is required")

    if not settings.QDRANT_URL:
        errors.append("QDRANT_URL is required")

    if not settings.QDRANT_API_KEY:
        errors.append("QDRANT_API_KEY is required")

    # OpenAI API key is only required if using OpenAI embeddings
    if settings.EMBEDDING_TYPE.lower() == "openai" and not settings.OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is required when using OpenAI embeddings")
    
    # Cohere API key is only required if using Cohere embeddings
    if settings.EMBEDDING_TYPE.lower() == "cohere" and not settings.COHERE_API_KEY:
        errors.append("COHERE_API_KEY is required when using Cohere embeddings")

    if errors:
        raise ValueError(f"Missing required environment variables: {', '.join(errors)}")


# Validate settings on import (but don't fail if .env doesn't exist yet)
try:
    validate_settings()
except ValueError as e:
    # Only raise if .env file exists but validation fails
    if ENV_FILE.exists():
        raise e
    # Otherwise, allow it to continue - validation will happen at runtime