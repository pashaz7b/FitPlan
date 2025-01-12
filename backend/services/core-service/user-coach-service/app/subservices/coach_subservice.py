from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends

from app.domain.models.fitplan_model import (Coach,
                                             CoachMetrics)
from app.infrastructure.repositories.coach_repository import CoachRepository
from app.subservices.auth.hash_subservice import HashService
from app.subservices.baseconfig import BaseService


class CoachSubService(BaseService):
    def __init__(self,
                 coach_repo: Annotated[CoachRepository, Depends()],
                 hash_subservice: Annotated[HashService, Depends()]
                 ) -> None:
        super().__init__()
        self.coach_repo = coach_repo
        self.hash_subservice = hash_subservice

    # async def create_coach(self, coach_struct: CoachRegisterSchema) -> Coach:
    #     logger.info(f"[+] Creating Coach With Email ---> {coach_struct.email}")
    #     new_coach = Coach(
    #         password=self.hash_subservice.hash_password(coach_struct.password),
    #         user_name=coach_struct.user_name,
    #         name=coach_struct.name,
    #         email=coach_struct.email,
    #         phone_number=coach_struct.phone_number,
    #         gender=coach_struct.gender,
    #         date_of_birth=coach_struct.date_of_birth,
    #     )
    #
    #     created_coach = self.coach_repo.create_coach(new_coach)
    #
    #     coach_metrics = CoachMetrics(
    #         coach_id=created_coach.id,
    #         height=coach_struct.height,
    #         weight=coach_struct.weight,
    #         specialization=coach_struct.specialization,
    #         biography=coach_struct.biography
    #     )
    #     self.coach_repo.create_coach_metrics(coach_metrics)
    #
    #     return created_coach

    async def update_coach(self, coach_id: int, update_fields: Dict) -> Coach:
        logger.info(f"Updating coach with id {coach_id}")
        return self.coach_repo.update_coach(coach_id, update_fields)

    async def update_coach_by_email(self, email: str, update_fields: Dict) -> Coach:
        logger.info(f"Updating coach with Email ---> {email}")
        return self.coach_repo.update_coach_by_email(email, update_fields)

    async def delete_coach(self, coach: Coach) -> None:
        logger.info(f"Deleting coach with id {coach.id}")
        return self.coach_repo.delete_coach(coach)

    async def get_coach(self, coach_id: int) -> Coach:
        logger.info(f"Fetching coach with id {coach_id}")
        return self.coach_repo.get_coach(coach_id)

    async def get_coach_by_email(self, email: str) -> Coach:
        logger.info(f"[+] Fetching coach with Email ---> {email}")
        return self.coach_repo.get_coach_by_email(email)

    async def get_coach_user(self, coach_id: int):
        logger.info(f"Fetching coach user with coach_id {coach_id}")
        return self.coach_repo.get_coach_user(coach_id)

    async def get_coach_user_meal_request(self, coach_id: int):
        logger.info(f"Fetching coach user meal request with coach_id {coach_id}")
        return self.coach_repo.get_coach_user_meal_request(coach_id)