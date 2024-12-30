from typing import Annotated
from loguru import logger
from fastapi import Depends

from app.subservice.user_subservice import UserSubService


class UserProfile():
    def __init__(self, user_subservice: Annotated[UserSubService, Depends()],
                 ) -> None:
        super().__init__()
        self.user_subservice = user_subservice

    async def change_profile(self, user_email: str, update_fields: dict):
        logger.info(f"Updating user with email {user_email}")
        return await self.user_subservice.update_user_by_email(user_email, update_fields)

    async def get_user_profile(self, user_email: str):
        logger.info(f"Retrieving user with email {user_email}")
        return await self.user_subservice.get_user_by_email(user_email)

    async def send_meal_media(self, user_email: str, update_fields: dict):
        logger.info(f"[+] Uploading User Meal With Email ---> {user_email}")
        return await self.user_subservice.update_user_by_email(user_email, update_fields)
