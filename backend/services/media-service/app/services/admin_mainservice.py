from typing import Annotated
from loguru import logger
from fastapi import Depends
from fastapi import HTTPException
from bson import ObjectId

from app.subservice.admin_subservice import AdminSubService
from app.subservice.user_subservice import UserSubService
from app.subservice.coach_subservice import CoachSubService


class AdminProfile():
    def __init__(self, admin_subservice: Annotated[AdminSubService, Depends()],
                 user_subservice: Annotated[UserSubService, Depends()],
                 coach_subservice: Annotated[CoachSubService, Depends()]
                 ) -> None:
        super().__init__()
        self.admin_subservice = admin_subservice
        self.user_subservice = user_subservice
        self.coach_subservice = coach_subservice

    async def change_admin_profile(self, admin_email: str, update_fields: dict):
        logger.info(f"Updating Admin with email {admin_email}")
        return await self.admin_subservice.update_admin_by_email(admin_email, update_fields)

    async def get_admin_profile(self, admin_email: str):
        logger.info(f"Retrieving Admin with email {admin_email}")
        return await self.admin_subservice.get_admin_by_email(admin_email)

    async def admin_get_user_profile(self, user_email: str):
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

    async def admin_get_coach_profile(self, coach_email: str):
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
