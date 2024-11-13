from functools import lru_cache
from pathlib import Path

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
    JWT_SECRET_KEY: str = "1807372bcbf0963ebe30a1df3669690b8f0e4f83a1b52e7579cfee9ff08db230"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OTP_EXPIRE_TIME: int = 60
    #*************************
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "your_email@gmail.com"
    SMTP_PASSWORD: str = "your_email_password"
    EMAIL_FROM: str = "your_email@gmail.com"
    # model_config = SettingsConfigDict(env_file=str(Path(__file__).resolve().parent / ".env"))


#@lru_cache
@logger.catch
def get_settings():
    return Settings()
