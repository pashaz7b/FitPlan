from typing import Annotated
from loguru import logger
from fastapi import Depends

from app.subservice.coach_subservice import CoachSubService


class CoachProfile():
    def __init__(self, coach_subservice: Annotated[CoachSubService, Depends()],
                 ) -> None:
        super().__init__()
        self.coach_subservice = coach_subservice

    async def change_coach_profile(self, coach_email: str, update_fields: dict):
        logger.info(f"Updating Coach with email {coach_email}")
        return await self.coach_subservice.update_coach_by_email(coach_email, update_fields)

    async def get_coach_profile(self, coach_email: str):
        logger.info(f"Retrieving Coach with email {coach_email}")
        return await self.coach_subservice.get_coach_by_email(coach_email)
