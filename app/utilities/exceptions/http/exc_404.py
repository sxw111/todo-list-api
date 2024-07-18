from fastapi import HTTPException, status

from app.utilities.messages.exc_details import (http_404_id_details,
                                                http_404_todo_id_details,
                                                http_404_todos_details)


async def http_404_exc_id_not_found_request(user_id: int) -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=http_404_id_details(user_id=user_id),
    )


async def http_404_exc_todo_id_not_found_request(todo_id: int) -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=http_404_todo_id_details(todo_id=todo_id),
    )


async def http_404_exc_todos_not_found_request() -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=http_404_todos_details()
    )
