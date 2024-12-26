from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends

from app.domain.models.user_model import User
from app.domain.models.user_model import UserMetrics
from app.infrastructure.repositories.user_repository import UserRepository


class UserSubService():
    def __init__(self,
                 user_repo: Annotated[UserRepository, Depends()],
                 ) -> None:
        super().__init__()
        self.user_repo = user_repo

    async def update_user(self, user_id: int, update_fields: Dict) -> User:
        logger.info(f"Updating user with id {user_id}")
        return self.user_repo.update_user(user_id, update_fields)

    async def update_user_by_email(self, email: str, update_fields: Dict) -> User:
        logger.info(f"Updating user with Email ---> {email}")
        return self.user_repo.update_user_by_email(email, update_fields)

    async def get_user(self, user_id: int) -> User:
        logger.info(f"Fetching user with id {user_id}")
        return self.user_repo.get_user(user_id)

    async def get_user_by_email(self, email: str) -> User:
        logger.info(f"[+] Fetching user with Email ---> {email}")
        return self.user_repo.get_user_by_email(email)
