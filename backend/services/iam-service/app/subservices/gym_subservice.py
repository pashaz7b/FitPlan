from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends

from app.domain.models.gym_model import Gym
from app.domain.schemas.gym_schema import GymRegisterSchema
from app.infrastructure.repositories.gym_repository import GymRepository
from app.subservices.baseconfig import BaseService


class GymSubService(BaseService):
    def __init__(self,
                 gym_repo: Annotated[GymRepository, Depends()],
                 ) -> None:
        super().__init__()
        self.gym_repo = gym_repo

    async def create_gym(self, coach_id: int, gym_register_schema: GymRegisterSchema) -> Gym:
        logger.info(f"[+] Creating Gyn With name  ---> {gym_register_schema.name}")

        gym = Gym(
            owner_id=coach_id,
            name=gym_register_schema.name,
            license_number=gym_register_schema.license_number,
            license_image=gym_register_schema.license_image,
            location=gym_register_schema.location,
            image=gym_register_schema.image,
            sport_facilities=gym_register_schema.sport_facilities,
            welfare_facilities=gym_register_schema.welfare_facilities,
        )

        created_gym = self.gym_repo.create_gym(gym)

        return created_gym
