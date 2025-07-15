# from functools import lru_cache
# from pathlib import Path

from loguru import logger

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_DIALECT: str = "postgresql+psycopg2"
    DATABASE_HOSTNAME: str = "postgres_container"
    DATABASE_NAME: str = "IAM-DB"
    DATABASE_PASSWORD: str = "admin"
    DATABASE_PORT: int = 5432
    DATABASE_USERNAME: str = "postgres"
    DEBUG_MODE: bool = False
    REDIS_URL: str = "localhost"
    # REDIS_URL: str = "redis"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/" #local
    JWT_SECRET_KEY: str = "1807372bcbf0963ebe30a1df3669690b8f0e4f83a1b52e7579cfee9ff08db230"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OTP_EXPIRE_TIME: int = 60
    #*************************
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = ""
    # *****************************************
    Password_OTP_EXPIRE_TIME: int = 120
    Password_TOKEN_EXPIRE_MINUTES: int = 10

    # model_config = SettingsConfigDict(env_file=str(Path(__file__).resolve().parent / ".env"))


#@lru_cache
@logger.catch
def get_settings():
    return Settings()
