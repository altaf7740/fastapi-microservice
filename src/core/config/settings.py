from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # CORE
    ENV: str
    APP_SECRET_KEY: str
    APP_LOG_LEVEL: str

    # DATABASE
    APP_DATABASE_URL: str
    APP_REDIS_URL: str

    # NETWORK
    APP_ALLOWED_HOSTS: list[str]
    APP_CORS_ORIGINS: list[str]
    APP_RESPONSE_TIMEOUT: int = 30

    # STATIC FILES
    STATIC_URL: str = "/static/"
    STATIC_DIR: Path = BASE_DIR / "static"
    DOCS_DIR: Path = STATIC_DIR / "docs"

    # Tracebacks and Logs
    APP_TRACEBACK_DEPTH: int

    model_config = {"extra": "allow"}


def reload_settings() -> Settings:
    load_dotenv(override=True)
    return Settings()  # type: ignore


settings = reload_settings()
