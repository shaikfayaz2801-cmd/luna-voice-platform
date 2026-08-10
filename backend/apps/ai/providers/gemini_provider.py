"""
Google Gemini AI Provider — Gemini 1.5 Pro with streaming and embeddings.
"""
import logging
from typing import AsyncGenerator
from django.conf import settings
from .base import BaseAIProvider

logger = logging.getLogger(__name__)


class GeminiProvider(BaseAIProvider):
    """Google Gemini 1.5 Pro provider with streaming and embeddings."""

    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.genai = genai
        self.model_name = settings.GEMINI_MODEL
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                'temperature': 0.85,
                'max_output_tokens': 1024,
            }
        )

    def _convert_messages(self, messages: list[dict]) -> tuple[str, list[dict]]:
        """Convert OpenAI-style messages to Gemini format."""
        system_prompt = ""
        gemini_messages = []

        for msg in messages:
            role = msg['role']
            content = msg['content']

            if role == 'system':
                system_prompt = content
            elif role == 'user':
                gemini_messages.append({'role': 'user', 'parts': [content]})
            elif role == 'assistant':
                gemini_messages.append({'role': 'model', 'parts': [content]})

        return system_prompt, gemini_messages

    async def complete(
        self, messages: list[dict], stream: bool = True
    ) -> AsyncGenerator[str, None]:
        """Stream or batch complete with Gemini."""
        try:
            system_prompt, gemini_messages = self._convert_messages(messages)

            # Build model with system instruction
            model = self.genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt,
                generation_config={'temperature': 0.85, 'max_output_tokens': 1024},
            )

            chat = model.start_chat(history=gemini_messages[:-1] if gemini_messages else [])
            last_user_message = gemini_messages[-1]['parts'][0] if gemini_messages else ""

            if stream:
                response = await chat.send_message_async(last_user_message, stream=True)
                async for chunk in response:
                    if chunk.text:
                        yield chunk.text
            else:
                response = await chat.send_message_async(last_user_message)
                yield response.text or ""

        except Exception as e:
            logger.exception(f"Gemini completion error: {e}")
            yield "I'm sorry, I'm having trouble connecting right now. Please try again in a moment."

    async def get_embedding(self, text: str) -> list[float]:
        """Generate embedding using Gemini embedding model."""
        try:
            result = await self.genai.embed_content_async(
                model='models/embedding-001',
                content=text[:10000],
                task_type='retrieval_document',
            )
            return result['embedding']
        except Exception as e:
            logger.exception(f"Gemini embedding error: {e}")
            return []
