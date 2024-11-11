from databases import DatabaseURL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from loguru import logger

DATABASE_URL = "postgresql://postgres:admin@localhost/fitplan_db"
engine = create_engine(DATABASE_URL, future=True)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()