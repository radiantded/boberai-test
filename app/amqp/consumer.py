import asyncio
from typing import Annotated

from faststream import AckPolicy, Depends
from faststream.rabbit import RabbitBroker
from loguru import logger

from amqp.dependencies import get_task_repository
from api.schemas import TaskDTO
from db.repository import TaskRepository
from db.enums import TaskStatus
from settings.config import get_settings


settings = get_settings()
broker = RabbitBroker(url=settings.AMQP_DSN.encoded_string())


async def process_task(task: dict):
    """Имитация обработки задачи"""
    await asyncio.sleep(5)
    task.result = "Bober kurwa successfully deployed"



@broker.subscriber(
    queue=settings.DEFAULT_QUEUE,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def handle_tasks(
    repository: Annotated[TaskRepository, Depends(get_task_repository)],
    task: TaskDTO
):
    try:
        task.status = TaskStatus.processing
        await repository.update(task)
        await process_task(task)
    except Exception as ex:
        task.status = TaskStatus.failed
        logger.exception(f"Task [{task.id}] failed | {ex}")
    else:
        task.status = TaskStatus.done
        logger.success(f"Task [{task.id}] completed")
    finally:
        await repository.update(task)
        logger.info(f"Task [{task.id}] updated")


async def run_consumer():
    async with broker:
        await broker.start()
        logger.info("Consumer initialized")
        while True:
            await asyncio.sleep(1000)
