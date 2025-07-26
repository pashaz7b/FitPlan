#from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost/fitplan_chat"
#DATABASE_URL = "postgresql+asyncpg://postgres:admin@postgres_container:5432/fitplan_chat"
#DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost/fitplan_chat"


engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

EntityBase = declarative_base()

async def init_db() -> bool:
    async with engine.begin() as conn:
        await conn.run_sync(EntityBase.metadata.create_all)
    logger.info("Database Initialized")
    return True

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session