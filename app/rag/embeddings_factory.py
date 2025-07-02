from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain.embeddings.base import Embeddings

from app.core.config import settings


def get_embeddings() -> Embeddings:
    """
    Factory function to get the appropriate embeddings based on configuration.
    """
    if settings.LLM_PROVIDER == "openai":
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
        return OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
    
    elif settings.LLM_PROVIDER == "ollama":
        # Use Ollama embeddings - defaults to nomic-embed-text model
        return OllamaEmbeddings(
            base_url=settings.OLLAMA_API_BASE_URL,
            model="nomic-embed-text"  # A good embedding model for Ollama
        )
    
    else:
        # Default fallback to a simple embedding model for other providers
        # For now, use Ollama as it doesn't require API keys
        print(f"Warning: {settings.LLM_PROVIDER} embeddings not specifically configured. Using Ollama embeddings as fallback.")
        return OllamaEmbeddings(
            base_url=settings.OLLAMA_API_BASE_URL,
            model="nomic-embed-text"
        )
