from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str


class UserUpdate(BaseModel):
    username: str | None
    email: str | None
    password: str | None
