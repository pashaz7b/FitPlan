from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.postgres_db.postgres_database import get_db
from app.domain.models.fitplan_model import (User,
                                             UserMetrics,
                                             TransactionLog,
                                             UserTransactionLog)


class UserRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        logger.info(f"[+] User Created With Id ---> {user.id} And Email ---> {user.email}")
        return user

    def create_user_metrics(self, metrics: UserMetrics) -> UserMetrics:
        self.db.add(metrics)
        self.db.commit()
        self.db.refresh(metrics)
        logger.info(f"[+] Metrics Created For Coach Id ---> {metrics.user_id}")
        return metrics

    def update_user(self, user_id: int, updated_user: Dict):
        user_query = self.db.query(User).filter(User.id == user_id)
        db_user = user_query.first()
        user_query.filter(User.id == user_id).update(
            updated_user, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"[+] User With Id ---> {user_id} Updated")
        return db_user

    def update_user_metrics(self, user_id: int, updated_metrics: Dict):
        metrics_query = self.db.query(UserMetrics).filter(UserMetrics.user_id == user_id)
        db_metrics = metrics_query.first()
        metrics_query.filter(UserMetrics.user_id == user_id).update(
            updated_metrics, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_metrics)
        logger.info(f"[+] Metrics For User With Id ---> {user_id} Updated")
        return db_metrics

    def update_user_by_email(self, user_email: str, updated_user: Dict):
        user_query = self.db.query(User).filter(User.email == user_email)
        db_user = user_query.first()
        user_query.filter(User.email == user_email).update(
            updated_user, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"[+] User With Email ---> {user_email} Updated")
        return db_user

    def delete_user(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
        self.db.flush()
        logger.info(f"[+] User Deleted With Id ---> {user.id} And Email ---> {user.email}")

    def get_user(self, user_id: int):
        logger.info(f"[+] Fetching User With Id ---> {user_id}")
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_metrics(self, user_id: int):
        logger.info(f"[+] Fetching Metrics For User With Id ---> {user_id}")
        return self.db.query(UserMetrics).filter(UserMetrics.user_id == user_id).first()

    def get_user_by_email(self, email: str):
        logger.info(f"[+] Fetching User With Email --> {email}")
        return self.db.query(User).filter(User.email == email).first()

    def get_user_transaction_log(self, user_id: int):
        logger.info(f"[+] Fetching Transaction Log For User With Id ---> {user_id}")
        return (
            self.db.query(TransactionLog)
            .join(UserTransactionLog, TransactionLog.id == UserTransactionLog.transaction_id)
            .filter(UserTransactionLog.user_id == user_id)
            .all()
        )
