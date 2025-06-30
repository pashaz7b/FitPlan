from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.postgres_db.postgres_database import get_db
from app.domain.models.gym_model import Gym


class GymRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    # def update_coach(self, coach_id: int, updated_coach: Dict):
    #     coach_query = self.db.query(Coach).filter(Coach.id == coach_id)
    #     db_coach = coach_query.first()
    #     coach_query.filter(Coach.id == coach_id).update(
    #         updated_coach, synchronize_session=False
    #     )
    #     self.db.commit()
    #     self.db.refresh(db_coach)
    #     logger.info(f"[+] Coach With Id ---> {coach_id} Updated")
    #     return db_coach
    #
    # def update_coach_by_email(self, coach_email: str, updated_coach: Dict):
    #     coach_query = self.db.query(Coach).filter(Coach.email == coach_email)
    #     db_coach = coach_query.first()
    #     coach_query.filter(Coach.email == coach_email).update(
    #         updated_coach, synchronize_session=False
    #     )
    #     self.db.commit()
    #     self.db.refresh(db_coach)
    #     logger.info(f"[+] Coach With Email ---> {coach_email} Updated")
    #     return db_coach
    #
    # def get_coach(self, coach_id: int):
    #     logger.info(f"[+] Fetching Coach With Id ---> {coach_id}")
    #     return self.db.query(Coach).filter(Coach.id == coach_id).first()

    def get_gym(self, gym_id: int):
        logger.info(f"[+] Fetching Gym With Id ---> {gym_id}")
        return self.db.query(Gym).filter(Gym.id == gym_id).first()

    def update_gym(self, gym_id: int, updated_gym: Dict):
        gym_query = self.db.query(Gym).filter(Gym.id == gym_id)
        db_gym = gym_query.first()
        gym_query.filter(Gym.id == gym_id).update(
            updated_gym, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_gym)
        logger.info(f"[+] Gym With Id ---> {gym_id} Updated")
        return db_gym
