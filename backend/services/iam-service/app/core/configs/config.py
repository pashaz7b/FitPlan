from functools import lru_cache
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    # DATABASE_DIALECT: str = "postgresql+psycopg2"
    # DATABASE_HOSTNAME: str = "postgres_container"
    # DATABASE_NAME: str = "fitplan"
    # DATABASE_PASSWORD: str = "admin"
    # DATABASE_PORT: int = 5432
    # DATABASE_USERNAME: str = "postgres"
    # DEBUG_MODE: bool = False
    # model_config = SettingsConfigDict(env_file=str(Path(__file__).resolve().parent / ".env"))
    # ***********************************************************

    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")

    if ENVIRONMENT == "local":
        REDIS_URL: str = "localhost"  # local
        RABBITMQ_URL: str = "amqp://guest:guest@localhost/"  # local
        DATABASE_URL: str = "postgresql://postgres:admin@localhost/fitplan_db"  # local

    elif ENVIRONMENT == "docker":
        REDIS_URL: str = "redis"  # docker
        RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq/"  # docker
        DATABASE_URL: str = "postgresql://postgres:admin@postgres_container:5432/fitplan_db"  # docker

    JWT_SECRET_KEY: str = "1807372bcbf0963ebe30a1df3669690b8f0e4f83a1b52e7579cfee9ff08db230"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OTP_EXPIRE_TIME: int = 60
    # *************************
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    SMTP_USERNAME: str = "asldy3097@gmail.com"
    SMTP_PASSWORD: str = "xrtwqctuprcgeiyj"
    EMAIL_FROM: str = "asldy3097@gmail.com"
    # *****************************************
    Password_OTP_EXPIRE_TIME: int = 120
    Password_TOKEN_EXPIRE_MINUTES: int = 10


@lru_cache
@logger.catch
def get_settings():
    return Settings()
