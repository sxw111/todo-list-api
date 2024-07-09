from fastapi import APIRouter, status

from app.api.deps import SessionDep, CurrentUser
from app.models.schemas.user import UserOut, UserUpdate
from app.utilities.exceptions.http.exc_404 import http_404_exc_id_not_found_request
from app.utilities.exceptions.database import EntityDoesNotExist
from app.crud.user import (
    read_user_by_id,
    read_users,
    delete_user_by_id,
    update_user_by_id,
)


router = APIRouter()


@router.get("/", response_model=list[UserOut], status_code=status.HTTP_200_OK)
async def get_users(db: SessionDep) -> list[UserOut]:
    users = await read_users(db=db)

    return users


@router.get("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user(db: SessionDep, user_id: int) -> UserOut:
    try:
        user = await read_user_by_id(db=db, user_id=user_id)
    except EntityDoesNotExist:
        raise http_404_exc_id_not_found_request(user_id == user_id)

    return user


@router.patch("/", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user(
    db: SessionDep, current_user: CurrentUser, user_update: UserUpdate
) -> UserOut:
    try:
        updated_user = await update_user_by_id(
            db=db, user_id=current_user.id, user_update=user_update
        )
    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(user_id=current_user.id)

    return updated_user


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_user(db: SessionDep, current_user: CurrentUser) -> dict[str, str]:
    try:
        deletion_result = await delete_user_by_id(db=db, user_id=current_user.id)
    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(user_id=current_user.id)

    return {"notification": deletion_result}
