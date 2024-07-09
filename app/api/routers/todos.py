from fastapi import APIRouter, status

from app.models.schemas.todo import ToDoCreate, ToDoOut
from app.api.deps import SessionDep, CurrentUser
from app.crud.todo import (
    create_new_todo,
    read_todo_by_id,
    read_todos,
    update_todo_by_id,
    delete_todo_by_id,
)
from app.utilities.exceptions.database import EntityDoesNotExist
from app.utilities.exceptions.access import AccessDenied
from app.utilities.exceptions.http.exc_404 import (
    http_404_exc_todo_id_not_found_request,
    http_404_exc_todos_not_found_request,
)
from app.utilities.exceptions.http.exc_403 import http_403_exc_access_denied_request


router = APIRouter()


@router.get("/{todo_id}", response_model=ToDoOut, status_code=status.HTTP_200_OK)
async def get_todo(db: SessionDep, current_user: CurrentUser, todo_id: int) -> ToDoOut:
    try:
        todo = await read_todo_by_id(
            db=db, current_user_id=current_user.id, todo_id=todo_id
        )
    except EntityDoesNotExist:
        raise await http_404_exc_todo_id_not_found_request(todo_id=todo_id)
    except AccessDenied:
        raise await http_403_exc_access_denied_request()

    return todo


@router.get("/", response_model=list[ToDoOut], status_code=status.HTTP_200_OK)
async def get_todos(db: SessionDep, current_user: CurrentUser) -> list[ToDoOut]:
    try:
        todos = await read_todos(db=db, current_user_id=current_user.id)
    except EntityDoesNotExist:
        raise await http_404_exc_todos_not_found_request()

    return todos


@router.post("/", response_model=ToDoOut, status_code=status.HTTP_201_CREATED)
async def create_todo(
    db: SessionDep, current_user: CurrentUser, todo: ToDoCreate
) -> ToDoOut:
    todo = await create_new_todo(db=db, current_user_id=current_user.id, todo=todo)

    return todo


@router.put("/{todo_id}", response_model=ToDoOut, status_code=status.HTTP_200_OK)
async def update_todo(
    db: SessionDep, current_user: CurrentUser, todo_id: int
) -> ToDoOut:
    try:
        todo = await update_todo_by_id(
            db=db, current_user_id=current_user.id, todo_id=todo_id
        )
    except EntityDoesNotExist:
        raise http_404_exc_todo_id_not_found_request(todo_id=todo_id)
    except AccessDenied:
        raise http_403_exc_access_denied_request()

    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: SessionDep, current_user: CurrentUser, todo_id: int) -> None:
    try:
        await delete_todo_by_id(db=db, current_user_id=current_user.id, todo_id=todo_id)
    except EntityDoesNotExist:
        raise http_404_exc_todo_id_not_found_request(todo_id=todo_id)
    except AccessDenied:
        raise http_403_exc_access_denied_request()

    return None
