from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.postgres.postgres_database import get_db
from app.domain.models.user_model import User


class UserRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        logger.info(f"[+] User Created With Id ---> {user.id} And Email ---> {user.email}")
        return user

    def update_user(self, user_id: int, updated_user: Dict):
        user_query = self.db.query(User).filter(User.id == user_id)
        db_user = user_query.first()
        user_query.filter(User.id == user_id).update(
            updated_user, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"[+] User With Id ---> {user_id} updated")
        return db_user

    def delete_user(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
        self.db.flush()
        logger.info(f"[+] User Deleted With Id ---> {user.id} And Email ---> {user.email}")

    def get_user(self, user_id: int):
        logger.info(f"[+] Fetching User With Id ---> {user_id}")
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str):
        logger.info(f"[+] Fetching User With Email --> {email}")
        return self.db.query(User).filter(User.email == email).first()
