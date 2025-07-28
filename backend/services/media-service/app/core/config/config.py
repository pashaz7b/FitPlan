from functools import lru_cache
# from pathlib import Path
from loguru import logger
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")

    if ENVIRONMENT == "local":
        MONGO_DATABASE_URL: str = "mongodb://localhost:27017"
        IAM_URL: str = "http://iam.localhost"
        DATABASE_URL: str = "postgresql://postgres:admin@localhost/fitplan_db"

    elif ENVIRONMENT == "docker":
        MONGO_DATABASE_URL: str = "mongodb://mongo:27017"
        IAM_URL: str = "http://iam"
        DATABASE_URL: str = "postgresql://postgres:admin@postgres_container:5432/fitplan_db"

    # ************************************************
    DATABASE_NAME: str = "FitPlanMediaDB"
    FILE_STORAGE_PATH: str = "app/media"
    # IAM_URL: str = "http://localhost:8001"
    GRPC_PORT: int = "50051"

    # model_config = SettingsConfigDict(env_file=str(Path(__file__).resolve().parent / ".env"))


@lru_cache
@logger.catch
def get_settings():
    return Settings()
