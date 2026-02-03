import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import router
from amqp.consumer import run_consumer
from db.conn import engine
from db.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Обойдёмся без Alembic"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    lifespan=lifespan,
    root_path="/app",
    description="BoberAI"
)
app.include_router(router)


if __name__ == '__main__':
    asyncio.run(run_consumer())
