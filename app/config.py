from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    openrouter_api_key: str
    openrouter_model: str = "openai/gpt-4o-mini"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    memory_backend: str = "memory"  # "memory" or "redis"
    redis_url: str = "redis://localhost:6379"

    cors_origins: str = "*"
    log_level: str = "INFO"

    long_term_memory: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
