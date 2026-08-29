from functools import lru_cache
from os import environ

from pydantic import Field, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings

if not environ.get("POSTGRES_USER"):
    from dotenv import load_dotenv

    load_dotenv(".env.local")


class Settings(BaseSettings):
    APP_NAME: str = "LibTaskAPI"
    APP_VERSION: str = "0.1.0"

    DEBUG: bool = Field(default=False)

    # DB Connection
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DSN: PostgresDsn | None = None

    @field_validator("POSTGRES_DSN", mode="after")
    @classmethod
    def set_postgres_dsn(
        cls,
        current_value,
        info: ValidationInfo,
    ):
        if current_value:
            return current_value

        values = info.data

        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=values.get("POSTGRES_DB") or "",
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
