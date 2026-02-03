from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from db.enums import TaskStatus


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    payload: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.pending
    )
    result: Mapped[str] = mapped_column(String, nullable=True)
