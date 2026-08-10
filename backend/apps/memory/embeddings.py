"""
Embedding generation for memory storage and retrieval.
"""
import logging
import asyncio
from django.conf import settings

logger = logging.getLogger(__name__)


def get_embedding_sync(text: str) -> list[float]:
    """Synchronously generate an embedding vector for the given text."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(_get_embedding_async(text))
        finally:
            loop.close()
    except Exception as e:
        logger.exception(f"Sync embedding error: {e}")
        return []


async def _get_embedding_async(text: str) -> list[float]:
    """Async embedding generation using the configured AI provider."""
    from apps.ai.factory import get_ai_provider
    try:
        provider = get_ai_provider()
        return await provider.get_embedding(text)
    except Exception as e:
        logger.exception(f"Embedding generation error: {e}")
        return []


async def get_embedding_async(text: str) -> list[float]:
    """Public async interface for embedding generation."""
    return await _get_embedding_async(text)
