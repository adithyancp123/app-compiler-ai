"""Central settings and deterministic generation policy."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from env and defaults."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "ai-software-compiler"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./compiler.db"

    openai_base_url: str = "https://api.openai.com/v1"
    openai_api_key: str = "replace-me"
    openai_model: str = "gpt-4o-mini"

    default_temperature: float = 0.0
    max_repair_attempts: int = 2


@lru_cache
def get_settings() -> Settings:
    return Settings()
