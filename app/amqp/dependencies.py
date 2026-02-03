from typing import Annotated

from faststream import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.conn import session_maker
from db.repository import TaskRepository


async def get_db_session() -> AsyncSession:
    async with session_maker() as session:
        yield session


async def get_task_repository(
    session: Annotated[AsyncSession,
    Depends(get_db_session)]
) -> TaskRepository:
    return TaskRepository(session)