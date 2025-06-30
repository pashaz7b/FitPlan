from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends

from app.domain.models.gym_model import Gym
from app.infrastructure.repositories.gym_repository import GymRepository


class GymSubService():
    def __init__(self,
                 gym_repo: Annotated[GymRepository, Depends()],
                 ) -> None:
        super().__init__()
        self.gym_repo = gym_repo

    # async def update_coach(self, coach_id: int, update_fields: Dict) -> Coach:
    #     logger.info(f"Updating coach with id {coach_id}")
    #     return self.coach_repo.update_coach(coach_id, update_fields)
    #
    # async def update_coach_by_email(self, email: str, update_fields: Dict) -> Coach:
    #     logger.info(f"Updating coach with Email ---> {email}")
    #     return self.coach_repo.update_coach_by_email(email, update_fields)
    #
    # async def delete_coach(self, coach: Coach) -> None:
    #     logger.info(f"Deleting coach with id {coach.id}")
    #     return self.coach_repo.delete_coach(coach)
    #
    # async def get_coach(self, coach_id: int) -> Coach:
    #     logger.info(f"Fetching coach with id {coach_id}")
    #     return self.coach_repo.get_coach(coach_id)
    #
    # async def get_coach_by_email(self, email: str) -> Coach:
    #     logger.info(f"[+] Fetching coach with Email ---> {email}")
    #     return self.coach_repo.get_coach_by_email(email)

    async def get_gym(self, gym_id: int):
        logger.info(f"Fetching Gym With Id {gym_id}")
        return self.gym_repo.get_gym(gym_id)

    async def update_gym(self, gym_id: int, update_fields: Dict):
        logger.info(f"Updating Gym with id {gym_id}")
        return self.gym_repo.update_gym(gym_id, update_fields)
