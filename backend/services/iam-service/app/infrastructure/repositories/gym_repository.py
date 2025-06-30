from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.postgres.postgres_database import get_db
from app.domain.models.gym_model import Gym


class GymRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def create_gym(self, gym: Gym) -> Gym:
        self.db.add(gym)
        self.db.commit()
        self.db.refresh(gym)
        logger.info(f"[+] Gym Created With Id ---> {gym.id}")
        return gym