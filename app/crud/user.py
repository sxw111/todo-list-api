from pydantic import EmailStr
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash, verify_password
from app.models.db.user import User
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
    stmt = select(User).where(User.id == user_id)
    query = await db.execute(statement=stmt)
    user = query.scalar_one_or_none()

    if not user:
        raise EntityDoesNotExist(f"User with id `{user_id}` does not exist!")

    return user


async def read_user_by_username(db: AsyncSession, username: str) -> User:
    stmt = select(User).where(User.username == username)
    query = await db.execute(statement=stmt)
    user = query.scalar_one_or_none()

    if not user:
        raise EntityDoesNotExist(f"User with username `{username}` does not exist!")

    return user


async def read_user_by_email(db: AsyncSession, email: EmailStr) -> User:
    stmt = select(User).where(User.email == email)
    query = await db.execute(statement=stmt)
    user = query.scalar_one_or_none()

    if not user:
        raise EntityDoesNotExist(f"User with email `{email}` does not exist!")

    return user


async def read_users(db: AsyncSession) -> list[User]:
    stmt = select(User)
    query = await db.execute(statement=stmt)
    users = query.scalars().all()

    return users  # type: ignore


async def update_user_by_id(
    db: AsyncSession, user_id: int, user_update: UserUpdate
) -> User:
    new_user_data = user_update.model_dump()

    stmt = select(User).where(User.id == user_id)
    query = await db.execute(statement=stmt)
    update_user = query.scalar_one_or_none()

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
    stmt = select(User).where(User.id == user_id)
    query = await db.execute(statement=stmt)
    delete_user = query.scalar_one_or_none()

    if not delete_user:
        raise EntityDoesNotExist(f"User with id `{user_id}` does not exist!")

    await db.delete(delete_user)
    await db.commit()

    return f"Account with id '{user_id}' is successfully deleted!"


async def is_email_taken(db: AsyncSession, email: EmailStr) -> bool:
    stmt = select(User).where(User.email == email)
    query = await db.execute(statement=stmt)
    user = query.scalar_one_or_none()

    if user:
        raise EntityAlreadyExists(f"The email `{email}` is already registered!")

    return False


async def is_username_taken(db: AsyncSession, username: str) -> bool:
    stmt = select(User).where(User.username == username)
    query = await db.execute(statement=stmt)
    user = query.scalar_one_or_none()

    if user:
        raise EntityAlreadyExists(f"The username `{username}` is already registered!")

    return False


async def authenticate(db: AsyncSession, email: EmailStr, password: str) -> User:
    user = await read_user_by_email(db=db, email=email)

    if not verify_password(password, user.password):
        raise PasswordDoesNotMatch("Invalid password!")

    return user
