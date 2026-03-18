from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver

from app.config import get_settings


def get_checkpointer() -> BaseCheckpointSaver:
    """Return checkpointer based on MEMORY_BACKEND config."""
    settings = get_settings()

    if settings.memory_backend == "redis":
        try:
            from langgraph.checkpoint.redis import RedisSaver
        except ImportError as exc:
            raise RuntimeError(
                "MEMORY_BACKEND=redis requires 'langgraph-checkpoint-redis' to be installed."
            ) from exc

        checkpointer = RedisSaver(redis_url=settings.redis_url)
        checkpointer.setup()
        return checkpointer

    return InMemorySaver()


def get_store():
    """Return long-term memory store if enabled, else None."""
    settings = get_settings()

    if not settings.long_term_memory:
        return None

    from langgraph.store.memory import InMemoryStore

    # In production, replace with a DB-backed store
    return InMemoryStore()
