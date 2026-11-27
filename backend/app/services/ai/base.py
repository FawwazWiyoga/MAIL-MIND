from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseLLMProvider(ABC):
    """Abstract interface for all LLM providers (Gemini, Groq, OpenRouter)."""

    @abstractmethod
    async def generate_text(self, prompt: str, system_instruction: str | None = None) -> str:
        """Generate a simple text response."""
        pass

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        response_schema: Type[T],
        system_instruction: str | None = None,
    ) -> T:
        """Generate a strictly validated structured output matching the Pydantic schema."""
        pass
