from functools import lru_cache
# from pathlib import Path
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    #IAM_URL: str = "http://iam.localhost"
    IAM_URL:str = "http://iam"
    # ****************************************************
    #REDIS_URL: str = "localhost"
    REDIS_URL: str = "redis"
    JWT_SECRET_KEY: str = "1807372bcbf0963ebe30a1df3669690b8f0e4f83a1b52e7579cfee9ff08db230"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OTP_EXPIRE_TIME: int = 60
    # model_config = SettingsConfigDict(env_file=str(Path(__file__).resolve().parent / ".env"))
    # **********************************************************
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"  # local
    #RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq/"  # docker



@lru_cache
@logger.catch
def get_settings():
    return Settings()
