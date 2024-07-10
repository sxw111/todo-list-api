from datetime import datetime

from pydantic import BaseModel, Field


class ToDoCreate(BaseModel):
    title: str = Field("Veterinarian", description="Title of the todo")
    description: str = Field(
        "Take the cat to the vet", description="Description of the todo"
    )
    status: str = Field("TODO", description="Status of the todo")
    priority: str = Field("MEDIUM", description="Priority of the todo")
    due_date: datetime = Field(..., description="Due date of the todo")


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
