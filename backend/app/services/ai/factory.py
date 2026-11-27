from app.core.config import get_settings
from app.services.ai.base import BaseLLMProvider
from app.services.ai.gemini import GeminiProvider
from app.services.ai.openai_compat import OpenAICompatibleProvider

settings = get_settings()


def get_ai_provider(provider_name: str | None = None) -> BaseLLMProvider:
    """Factory to retrieve the configured or requested AI provider."""
    name = (provider_name or "gemini").lower()

    if name == "groq" and settings.GROQ_API_KEY:
        return OpenAICompatibleProvider(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
            model_name="llama-3.3-70b-versatile",
        )
    elif name == "openrouter" and settings.OPENROUTER_API_KEY:
        return OpenAICompatibleProvider(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            model_name="google/gemini-2.0-flash-001",
        )
    else:
        # Default to Gemini
        return GeminiProvider(model_name="gemini-1.5-flash")
