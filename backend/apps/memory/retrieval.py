"""
Memory retrieval using pgvector cosine similarity.
"""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def retrieve_relevant_memories_sync(user_id, query: str, limit: int = 5):
    """
    Retrieve the most relevant memories for a user given a query.
    Uses cosine similarity on pgvector embeddings.
    Falls back to recent memories if embedding fails.
    """
    from apps.memory.models import Memory

    try:
        # Get embedding for query
        from apps.memory.embeddings import get_embedding_sync
        query_embedding = get_embedding_sync(query)

        if query_embedding:
            from pgvector.django import CosineDistance
            memories = (
                Memory.objects.filter(user_id=user_id)
                .exclude(embedding=None)
                .annotate(distance=CosineDistance('embedding', query_embedding))
                .order_by('distance')[:limit]
            )
            return list(memories)

    except Exception as e:
        logger.warning(f"Vector search failed, falling back to recent: {e}")

    # Fallback: return most recent important memories
    return list(
        Memory.objects.filter(user_id=user_id)
        .order_by('-importance', '-created_at')[:limit]
    )


async def retrieve_relevant_memories_async(user_id, query: str, limit: int = 5):
    """Async wrapper for retrieval."""
    import asyncio
    return await asyncio.get_event_loop().run_in_executor(
        None, retrieve_relevant_memories_sync, user_id, query, limit
    )
