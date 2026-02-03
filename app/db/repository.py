from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import TaskCreate, TaskDTO

from db.models import Task


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: TaskCreate) -> Task:
        query = insert(Task).values(task.model_dump()).returning(Task)
        obj = await self.session.execute(query)
        await self.session.commit()
        task = obj.scalar_one()
        return TaskDTO(id=task.id, payload=task.payload)

    async def update(self, task: TaskDTO) -> None:
        stmt = update(Task).values(
            {"status": task.status, "result": task.result}
        ).where(Task.id == task.id)
        await self.session.execute(stmt)
        await self.session.commit()
