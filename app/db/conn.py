from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings.config import get_settings


settings = get_settings()
engine = create_async_engine(settings.PG_DSN.unicode_string(), pool_size=5)

session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
