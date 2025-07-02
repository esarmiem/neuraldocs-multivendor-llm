import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "RAG App"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # LLM
    LLM_PROVIDER: str = "ollama"  # openai, anthropic, gemini, ollama
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OLLAMA_API_BASE_URL: str = os.getenv("OLLAMA_API_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "deepseek-r1:8b")


    # Vector Store
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8002

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_very_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
