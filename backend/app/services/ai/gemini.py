import json
import logging
from typing import Type, TypeVar
from pydantic import BaseModel

import google.generativeai as genai
from app.core.config import get_settings
from app.services.ai.base import BaseLLMProvider

settings = get_settings()
logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class GeminiProvider(BaseLLMProvider):
    """Google Gemini AI Provider implementation."""

    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model_name = model_name
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)

    async def generate_text(self, prompt: str, system_instruction: str | None = None) -> str:
        if not settings.GEMINI_API_KEY:
            return "AI analysis unavailable: GEMINI_API_KEY is not configured in settings."

        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction,
            )
            response = await model.generate_content_async(prompt)
            return response.text or ""
        except Exception as e:
            logger.error(f"Gemini generate_text error: {e}")
            raise

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Type[T],
        system_instruction: str | None = None,
    ) -> T:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")

        full_system = (system_instruction or "") + (
            "\nYou MUST reply strictly in valid JSON adhering to the required schema. "
            "Do not include markdown code block formatting (e.g. ```json), return raw JSON only."
        )

        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=full_system,
                generation_config={"response_mime_type": "application/json"},
            )
            response = await model.generate_content_async(prompt)
            raw_text = response.text.strip()
            # Clean possible markdown block if provider leaked it
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]

            parsed_data = json.loads(raw_text.strip())
            return response_schema.model_validate(parsed_data)
        except Exception as e:
            logger.error(f"Gemini generate_structured error: {e}")
            raise
