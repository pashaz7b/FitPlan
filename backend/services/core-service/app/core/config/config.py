from functools import lru_cache
from pathlib import Path
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://localhost:27017"  # "mongodb://mongo:27017"
    DATABASE_NAME: str = "FitPlanMediaDB"
    TESSERACT_CMD: str = ""
    MEDIA_SERVICE_GRPC: str = ""
    IAM_URL: str = "http://iam"  # "http://iam.localhost"
    # *************************
    # REDIS_URL: str = "localhost"
    REDIS_URL: str = "redis"
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

    FitPlAN_PRICE: int = 1000000

    # model_config = SettingsConfigDict(env_file=str(Path(__file__).resolve().parent / ".env"))


@lru_cache
@logger.catch
def get_settings():
    return Settings()
