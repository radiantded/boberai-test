from fastapi import Depends
from faststream.rabbit.fastapi import RabbitRouter
from typing import Annotated

from api.dependencies import get_task_repository
from api.schemas import TaskCreate, TaskDTO
from db.repository import TaskRepository
from settings.config import get_settings


settings = get_settings()
router = RabbitRouter(url=settings.AMQP_DSN.encoded_string())


@router.post("/tasks", tags=["Tasks"])
async def receive_task(
    repository: Annotated[TaskRepository, Depends(get_task_repository)],
    task: TaskCreate
) -> TaskDTO:
    """Создать задачу"""
    task = await repository.create(task)
    await router.broker.publish(
        task,
        queue=settings.DEFAULT_QUEUE
    )
    return task
