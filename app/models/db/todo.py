from datetime import datetime
from enum import Enum

from sqlalchemy import TIMESTAMP, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class ToDoStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class ToDoPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ToDo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ToDoStatus] = mapped_column(default=ToDoStatus.TODO)
    priority: Mapped[ToDoPriority] = mapped_column(default=ToDoPriority.MEDIUM)
    due_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
