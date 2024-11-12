from typing import Annotated, Dict
from uuid import UUID
from loguru import logger
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.postgres.postgres_database import get_db
from app.domain.models.user_model import User


class UserRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def create_user(self, user: User) -> User:
        new_user = user
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    # def get_user_by_id(self, user_id: UUID) -> User:
    #     return self.db.query(User).filter(User.id == user_id).first()
    #
    # def get_user_by_email(self, email: str) -> User:
    #     return self.db.query(User).filter(User.email == email).first()
    #
    # def get_user_by_username(self, user_name: str) -> User:
    #     return self.db.query(User).filter(User.user_name == user_name).first()
    #
    # def update_user(self, user_id: UUID, user: Dict) -> User:
    #     user_to_update = self.get_user_by_id(user_id)
    #     for key, value in user.items():
    #         setattr(user_to_update, key, value)
    #     self.db.commit()
    #     self.db.refresh(user_to_update)
    #     return user_to_update
    #
    # def delete_user(self, user_id: UUID) -> User:
    #     user_to_delete = self.get_user_by_id(user_id)
    #     self.db.delete(user_to_delete)
    #     self.db.commit()
    #     return user_to_delete
