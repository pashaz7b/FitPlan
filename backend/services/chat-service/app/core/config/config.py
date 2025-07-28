from functools import lru_cache
# from pathlib import Path
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")

    if ENVIRONMENT == "local":
        REDIS_URL: str = "localhost"  # local
        RABBITMQ_URL: str = "amqp://guest:guest@localhost/"  # local
        DATABASE_URL: str = "postgresql+asyncpg://postgres:admin@localhost/fitplan_chat"  # local
        IAM_URL: str = "http://iam.localhost"  # local

    elif ENVIRONMENT == "docker":
        REDIS_URL: str = "redis"  # docker
        RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq/"  # docker
        DATABASE_URL: str = "postgresql+asyncpg://postgres:admin@postgres_container:5432/fitplan_chat"  # docker
        IAM_URL: str = "http://iam"  # docker

    # ****************************************************
    JWT_SECRET_KEY: str = "1807372bcbf0963ebe30a1df3669690b8f0e4f83a1b52e7579cfee9ff08db230"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OTP_EXPIRE_TIME: int = 60

    # model_config = SettingsConfigDict(env_file=str(Path(__file__).resolve().parent / ".env"))


@lru_cache
@logger.catch
def get_settings():
    return Settings()
