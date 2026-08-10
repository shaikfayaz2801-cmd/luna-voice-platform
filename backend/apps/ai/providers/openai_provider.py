"""
OpenAI AI Provider — GPT-4o with streaming support and embeddings.
"""
import logging
from typing import AsyncGenerator
from django.conf import settings
from .base import BaseAIProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseAIProvider):
    """OpenAI GPT-4o provider with streaming and embeddings."""

    def __init__(self):
        import openai
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.embedding_model = settings.OPENAI_EMBEDDING_MODEL

    async def complete(
        self, messages: list[dict], stream: bool = True
    ) -> AsyncGenerator[str, None]:
        """Stream or batch complete with GPT-4o."""
        try:
            if stream:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=True,
                    temperature=0.85,
                    max_tokens=1024,
                )
                async for chunk in response:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        yield delta.content
            else:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=False,
                    temperature=0.85,
                    max_tokens=1024,
                )
                yield response.choices[0].message.content or ""
        except Exception as e:
            logger.exception(f"OpenAI completion error: {e}")
            yield "I'm sorry, I'm having trouble connecting right now. Please try again in a moment."

    async def get_embedding(self, text: str) -> list[float]:
        """Generate text embedding using text-embedding-3-small."""
        try:
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=text[:8000],  # Truncate to model limit
            )
            return response.data[0].embedding
        except Exception as e:
            logger.exception(f"OpenAI embedding error: {e}")
            return []
