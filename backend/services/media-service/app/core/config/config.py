from functools import lru_cache
from pathlib import Path
from loguru import logger

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str =  "mongodb://localhost:27017"   #"mongodb://mongo:27017"
    DATABASE_NAME: str = "FitPlanMediaDB"
    FILE_STORAGE_PATH: str = "app/media"
    IAM_URL: str = "http://iam.localhost"
    GRPC_PORT: int = "50051"

    # model_config = SettingsConfigDict(env_file=str(Path(__file__).resolve().parent / ".env"))


#@lru_cache
@logger.catch
def get_settings():
    return Settings()
