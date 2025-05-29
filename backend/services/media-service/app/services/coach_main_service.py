from typing import Annotated
from loguru import logger
from fastapi import Depends
from fastapi import HTTPException
from bson import ObjectId

from app.subservice.coach_subservice import CoachSubService
from app.subservice.user_subservice import UserSubService


class CoachProfile():
    def __init__(self, coach_subservice: Annotated[CoachSubService, Depends()],
                 user_subservice: Annotated[UserSubService, Depends()]
                 ) -> None:
        super().__init__()
        self.coach_subservice = coach_subservice
        self.user_subservice = user_subservice

    async def change_coach_profile(self, coach_email: str, update_fields: dict):
        logger.info(f"Updating Coach with email {coach_email}")
        return await self.coach_subservice.update_coach_by_email(coach_email, update_fields)

    async def get_coach_profile(self, coach_email: str):
        logger.info(f"Retrieving Coach with email {coach_email}")
        return await self.coach_subservice.get_coach_by_email(coach_email)

    async def coach_get_user_profile(self, user_email: str):
        logger.info(f"Retrieving User with email {user_email}")
        fetched_user = await self.user_subservice.get_user_by_email(user_email)

        if not fetched_user:
            logger.error(f"No user found with email {user_email}")
            raise HTTPException(
                status_code=404,
                detail=f"No user found with email {user_email}"
            )

        if not fetched_user.image:
            raise HTTPException(
                status_code=404,
                detail="No image found for the specified user"
            )

        mongo_id = ObjectId(fetched_user.image)
        return mongo_id
