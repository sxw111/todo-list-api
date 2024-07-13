from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
import decouple


class Settings(BaseSettings):
    TITLE: str = "Todo list application"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "UTC"
    DESCRIPTION: str | None = None
    DEBUG: bool = False

    DATABASE_URL: PostgresDsn

    ACCESS_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_DAYS: int

    IS_ALLOWED_CREDENTIALS: bool = decouple.config("IS_ALLOWED_CREDENTIALS", cast=bool)
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://0.0.0.0:3000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://localhost:5173",
        "http://0.0.0.0:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
