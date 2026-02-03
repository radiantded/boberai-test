from functools import lru_cache

from pydantic import PostgresDsn, AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PG_DSN: PostgresDsn = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
    AMQP_DSN: AmqpDsn = "amqp://guest:guest@rabbit:5672/"

    DEFAULT_QUEUE: str = "tasks"


@lru_cache
def get_settings() -> Settings:
    return Settings()
