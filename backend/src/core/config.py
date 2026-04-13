import os
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_STORAGE = BASE_DIR / "storage" / "files"
DEFAULT_STORAGE.mkdir(parents=True, exist_ok=True)

class Settings(BaseSettings):

    DB_URL: str = (
        f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:"
        f"{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:"
        f"{os.environ.get('PGPORT')}/{os.environ.get('POSTGRES_DB')}"
    )

    CORS_ORIGINS: str = os.environ.get(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000"
    ).split(",")


    STORAGE_DIR: Path = os.environ.get("STORAGE_DIR", str(DEFAULT_STORAGE))
    REDIS_URL: str  = os.environ.get("REDIS_URL", "redis://backend-redis:6379/0")

settings = Settings()
