from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.postgres_db.postgres_database import get_db
from app.domain.models.fitplan_model import UserDuplicates


class UserDuplicatesRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def get_user_by_email(self, email: str):
        user = self.db.query(UserDuplicates).filter(UserDuplicates.email == email).first()
        return user

    def get_user_by_phone_number(self, phone_number: str):
        user = self.db.query(UserDuplicates).filter(UserDuplicates.phone_number == phone_number).first()
        return user

    def get_user_by_user_name(self, user_name: str):
        user = self.db.query(UserDuplicates).filter(UserDuplicates.user_name == user_name).first()
        return user
