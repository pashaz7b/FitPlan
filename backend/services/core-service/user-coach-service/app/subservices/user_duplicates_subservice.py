from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends

from app.infrastructure.repositories.user_duplicate_repository import UserDuplicatesRepository


class UserDuplicatesSubService():
    def __init__(self,
                 user_duplicates_repo: Annotated[UserDuplicatesRepository, Depends()]
                 ) -> None:
        self.user_duplicates_repo = user_duplicates_repo

    async def get_user_by_email(self, email: str):
        logger.info(f"[+] Fetching User with Email ---> {email}")
        return self.user_duplicates_repo.get_user_by_email(email)

    async def get_user_by_phone_number(self, phone_number: str):
        logger.info(f"[+] Fetching User with Phone Number ---> {phone_number}")
        return self.user_duplicates_repo.get_user_by_phone_number(phone_number)

    async def get_user_by_user_name(self, user_name: str):
        logger.info(f"[+] Fetching User with User Name ---> {user_name}")
        return self.user_duplicates_repo.get_user_by_user_name(user_name)