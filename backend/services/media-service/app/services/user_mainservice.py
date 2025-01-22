from typing import Annotated
from loguru import logger
from fastapi import Depends
from fastapi import HTTPException
from bson import ObjectId

from app.subservice.user_subservice import UserSubService
from app.subservice.coach_subservice import CoachSubService


class UserProfile():
    def __init__(self, user_subservice: Annotated[UserSubService, Depends()],
                 coach_subservice: Annotated[CoachSubService, Depends()]
                 ) -> None:
        super().__init__()
        self.user_subservice = user_subservice
        self.coach_subservice = coach_subservice

    async def change_profile(self, user_email: str, update_fields: dict):
        logger.info(f"Updating user with email {user_email}")
        return await self.user_subservice.update_user_by_email(user_email, update_fields)

    async def get_user_profile(self, user_email: str):
        logger.info(f"Retrieving user with email {user_email}")
        return await self.user_subservice.get_user_by_email(user_email)

    async def send_meal_media(self, user_email: str, update_fields: dict):
        logger.info(f"[+] Uploading User Meal With Email ---> {user_email}")
        return await self.user_subservice.update_user_by_email(user_email, update_fields)

    async def user_get_coach_profile(self, coach_email: str):
        logger.info(f"Retrieving Coach with email {coach_email}")
        fetched_coach = await self.coach_subservice.get_coach_by_email(coach_email)

        if not fetched_coach:
            logger.error(f"No coach found with email {coach_email}")
            raise HTTPException(
                status_code=404,
                detail=f"No coach found with email {coach_email}"
            )

        if not fetched_coach.image:
            raise HTTPException(
                status_code=404,
                detail="No image found for the specified coach"
            )

        mongo_id = ObjectId(fetched_coach.image)
        return mongo_id
