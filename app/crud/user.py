from pydantic import EmailStr
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash, verify_password
from app.models.db.models import User
from app.models.schemas.user import UserCreate, UserUpdate
from app.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from app.utilities.exceptions.password import PasswordDoesNotMatch


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    new_user = User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def read_user_by_id(db: AsyncSession, user_id: int) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise EntityDoesNotExist(f"User with id `{user_id}` does not exist!")

    return user


async def read_user_by_username(db: AsyncSession, username: str) -> User:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if not user:
        raise EntityDoesNotExist(f"User with username `{username}` does not exist!")

    return user


async def read_user_by_email(db: AsyncSession, email: EmailStr) -> User:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise EntityDoesNotExist(f"User with email `{email}` does not exist!")

    return user


async def read_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    users = result.scalars().all()

    return users


async def update_user_by_id(
    db: AsyncSession, user_id: int, user_update: UserUpdate
) -> User:
    new_user_data = user_update.model_dump()

    result = await db.execute(select(User).where(User.id == user_id))
    update_user = result.scalar_one_or_none()

    if not update_user:
        raise EntityDoesNotExist(f"User with id `{user_id}` does not exist!")

    update_stmt = update(table=User).where(User.id == update_user.id)

    if new_user_data["username"]:
        update_stmt = update_stmt.values(username=new_user_data["username"])

    if new_user_data["email"]:
        update_stmt = update_stmt.values(email=new_user_data["email"])

    if new_user_data["password"]:
        hashed_password = get_password_hash(new_user_data["password"])
        update_stmt = update_stmt.values(password=hashed_password)

    await db.execute(statement=update_stmt)
    await db.commit()
    await db.refresh(update_user)

    return update_user


async def delete_user_by_id(db: AsyncSession, user_id: int) -> str:
    result = await db.execute(select(User).where(User.id == user_id))
    delete_user = result.scalar_one_or_none()

    if not delete_user:
        raise EntityDoesNotExist(f"User with id `{user_id}` does not exist!")

    await db.delete(delete_user)
    await db.commit()

    return f"Account with id '{user_id}' is successfully deleted!"


async def is_email_taken(db: AsyncSession, email: EmailStr) -> bool:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user:
        raise EntityAlreadyExists(f"The email `{email}` is already registered!")

    return False


async def is_username_taken(db: AsyncSession, username: str) -> bool:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user:
        raise EntityAlreadyExists(f"The username `{username}` is already registered!")

    return False


async def authenticate(db: AsyncSession, email: EmailStr, password: str) -> User:
    user = await read_user_by_email(db=db, email=email)

    if not verify_password(password, user.password):
        raise PasswordDoesNotMatch("Invalid password!")

    return user
