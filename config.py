from functools import lru_cache
from logging.config import dictConfig
from pathlib import Path
from typing import Any

from decouple import config
from pydantic import BaseSettings, Field, PostgresDsn, validator

BASEDIR = Path.cwd()

LOG_LEVEL = config("LOG_LEVEL", default="debug").upper()
LOG_DIR = BASEDIR / "logs"


dictConfig(
    dict(
        version=1,
        formatters={
            "default": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
            },
            "rich": {"datefmt": "[%X]"},
        },
        handlers={
            "console": {
                "class": "rich.logging.RichHandler",
                "formatter": "rich",
                "level": "DEBUG",
                "rich_tracebacks": True,
            },
            "file": {
                "level": "DEBUG",
                "formatter": "default",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": LOG_DIR / "app.log",
                "when": "D",
                "interval": 1,
                "backupCount": 7,
            },
        },
        root={"handlers": ["console"], "level": "DEBUG"},
        loggers={
            "app": {
                "level": LOG_LEVEL,
                "handlers": ["console", "file"],
                "propagate": False,
            }
        },
    )
)


class Config(BaseSettings):
    VERSION: str = Field(default="v1", env="VERSION")
    DEBUG: bool = Field(default=False, env="DEBUG")

    POSTGRES_USER: str = Field(default="", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(default="", env="POSTGRES_PASSWORD")
    POSTGRES_HOST: str = Field(default="", env="POSTGRES_HOST")
    POSTGRES_PORT: str = Field(default="", env="POSTGRES_PORT")
    POSTGRES_DB: str = Field(default="", env="POSTGRES_DB")
    DATABASE_URL: str | None

    @validator("DATABASE_URL", pre=True)
    def build_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if v:
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                user=values.get("POSTGRES_USER"),
                password=values.get("POSTGRES_PASSWORD"),
                host=values.get("POSTGRES_HOST"),
                port=str(values.get("POSTGRES_PORT")),
                path=f"/{values.get('POSTGRES_DB') or ''}",
            )
        )

    class Config:
        env_file = ".env"


class TestingConfig(Config):
    @validator("DATABASE_URL", pre=True)
    def build_db_connection(cls, v: str | None) -> Any:
        return "sqlite+aiosqlite://"


@lru_cache
def get_config():
    return Config()


@lru_cache
def get_testing_config():
    return TestingConfig()


CONFIG = get_config()
TESTING_CONFIG = get_testing_config()
