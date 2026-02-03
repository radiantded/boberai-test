from pydantic import BaseModel

from db.enums import TaskStatus


class TaskCreate(BaseModel):
    payload: str


class TaskDTO(TaskCreate):
    id: int = None
    status: TaskStatus = TaskStatus.pending
    result: str | None = None
