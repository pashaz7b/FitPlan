from databases import DatabaseURL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from loguru import logger

DATABASE_URL = "postgresql://postgres:admin@localhost/fitplan_chat_db"
#DATABASE_URL = "postgresql://postgres:admin@postgres_container:5432/fitplan_db"
engine = create_engine(DATABASE_URL, future=True)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

EntityBase = declarative_base()


def init_db() -> bool:
    EntityBase.metadata.create_all(bind=engine)
    logger.info("Database Initialized")
    return True


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
