from datetime import datetime

from pydantic import BaseModel


class ToDoCreate(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    due_date: datetime


class ToDoOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    due_date: datetime
    created_at: datetime
    updated_at: datetime
    owner_id: int


class ToDoUpdate(BaseModel):
    title: str | None
    description: str | None
    status: str | None
    priority: str | None
    due_date: datetime | None
