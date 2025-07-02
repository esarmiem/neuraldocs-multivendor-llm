from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from app.core.config import settings

def get_llm():
    """Factory function to get the LLM based on the provider."""
    provider = settings.LLM_PROVIDER.lower()

    if provider == "openai":
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")
        return ChatOpenAI(api_key=settings.OPENAI_API_KEY)

    elif provider == "anthropic":
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is not set")
        return ChatAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    elif provider == "gemini":
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set")
        return ChatGoogleGenerativeAI(google_api_key=settings.GEMINI_API_KEY, model="gemini-pro")

    elif provider == "ollama":
        return OllamaLLM(
            base_url=settings.OLLAMA_API_BASE_URL,
            model=settings.OLLAMA_MODEL,
        )

    else:
        raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")

llm = get_llm()
