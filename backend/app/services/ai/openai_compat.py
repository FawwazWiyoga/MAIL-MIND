import json
import logging
from typing import Type, TypeVar
from pydantic import BaseModel
from openai import AsyncOpenAI

from app.core.config import get_settings
from app.services.ai.base import BaseLLMProvider

settings = get_settings()
logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class OpenAICompatibleProvider(BaseLLMProvider):
    """Generic provider for OpenAI-compatible APIs (Groq, OpenRouter)."""

    def __init__(self, api_key: str, base_url: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    async def generate_text(self, prompt: str, system_instruction: str | None = None) -> str:
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAICompatible generate_text error: {e}")
            raise

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Type[T],
        system_instruction: str | None = None,
    ) -> T:
        full_system = (system_instruction or "") + (
            f"\nYou must return ONLY a valid JSON object matching this schema:\n"
            f"{json.dumps(response_schema.model_json_schema())}\n"
            "Do not include any explanation or markdown formatting."
        )

        messages = [
            {"role": "system", "content": full_system},
            {"role": "user", "content": prompt},
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content or "{}"
            parsed = json.loads(content)
            return response_schema.model_validate(parsed)
        except Exception as e:
            logger.error(f"OpenAICompatible generate_structured error: {e}")
            raise
