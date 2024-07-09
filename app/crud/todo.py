from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from app.models.db.models import ToDo
from app.models.schemas.todo import ToDoCreate, ToDoUpdate
from app.utilities.exceptions.database import EntityDoesNotExist
from app.utilities.exceptions.access import AccessDenied


async def create_new_todo(
    db: AsyncSession, current_user_id: int, todo: ToDoCreate
) -> ToDo:
    new_todo = ToDo(**todo.model_dump(), owner_id=current_user_id)

    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)

    return new_todo


async def read_todo_by_id(db: AsyncSession, current_user_id: int, todo_id: int) -> ToDo:
    result = await db.execute(select(ToDo).where(ToDo.id == todo_id))
    todo = result.scalar_one_or_none()

    if not todo:
        raise EntityDoesNotExist(f"Todo with id `{id}` does not exist!")

    if todo.owner_id != current_user_id:
        raise AccessDenied("You don't have access to other people's todos")

    return todo


async def read_todos(db: AsyncSession, current_user_id: int) -> list[ToDo]:
    result = await db.execute(select(ToDo).where(ToDo.owner_id == current_user_id))
    todos = result.scalars().all()

    if not todos:
        raise EntityDoesNotExist("You don't have todos!")

    return todos


async def update_todo_by_id(
    db: AsyncSession, current_user_id: int, todo_id: int, todo_update: ToDoUpdate
) -> ToDo:
    new_todo_data = todo_update.model_dump()

    result = await db.execute(select(ToDo).where(ToDo.id == todo_id))
    update_todo = result.scalar_one_or_none()

    if not update_todo:
        raise EntityDoesNotExist(f"Todo with id `{id}` does not exist!")

    if update_todo.owner_id != current_user_id:
        raise AccessDenied("You don't have access to other people's todos")

    update_stmt = update(table=ToDo).where(ToDo.id == update_todo)

    if new_todo_data["title"]:
        update_stmt = update_stmt.values(title=new_todo_data["title"])

    if new_todo_data["description"]:
        update_stmt = update_stmt.values(title=new_todo_data["description"])

    if new_todo_data["status"]:
        update_stmt = update_stmt.values(title=new_todo_data["status"])

    if new_todo_data["priority"]:
        update_stmt = update_stmt.values(title=new_todo_data["priority"])

    if new_todo_data["due_date"]:
        update_stmt = update_stmt.values(title=new_todo_data["due_date"])

    await db.execute(statement=update_stmt)
    await db.commit()
    await db.refresh(update_todo)

    return update_todo


async def delete_todo_by_id(
    db: AsyncSession, current_user_id: int, todo_id: int
) -> None:
    todo = await read_todo_by_id(
        db=db, current_user_id=current_user_id, todo_id=todo_id
    )

    await db.delete(todo)
    await db.commit()

    return None
