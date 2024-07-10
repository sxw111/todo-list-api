from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field("Tom", description="User name")
    email: str = Field("tom@gmail.com", description="User email")
    password: str = Field("12345", description="User password")


class UserOut(BaseModel):
    id: int
    username: str
    email: str


class UserUpdate(BaseModel):
    username: str | None
    email: str | None
    password: str | None
