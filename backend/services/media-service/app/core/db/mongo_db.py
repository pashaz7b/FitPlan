from motor.motor_asyncio import AsyncIOMotorClient
from loguru import logger
from app.core.config.config import get_settings

try:
    config = get_settings()
    client = AsyncIOMotorClient(config.DATABASE_URL)
    db = client[config.DATABASE_NAME]
    logger.info("[+] Connected To Mongo Database")
except Exception as e:
    logger.error(f"[+] Error Connecting To Mongo Database: {e}")


async def get_db():
    yield db
