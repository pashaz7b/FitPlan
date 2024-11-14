from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends

from app.domain.models.user_model import User
from app.domain.schemas.user_schema import UserRegisterSchema
from app.infrastructure.repositories.user_repository import UserRepository
from app.subservices.auth.hash_subservice import HashService
from app.subservices.baseconfig import BaseService


class UserSubService(BaseService):
    def __init__(self,
                 user_repo: Annotated[UserRepository, Depends()],
                 hash_subservice: Annotated[HashService, Depends()]
                 ) -> None:
        super().__init__()
        self.user_repo = user_repo
        self.hash_subservice = hash_subservice

    async def create_user(self, user_struct: UserRegisterSchema) -> User:
        logger.info(f"[+] Creating User With Email ---> {user_struct.email}")
        new_user = User(password=self.hash_subservice.hash_password(user_struct.password),
                        user_name=user_struct.user_name,
                        name=user_struct.name,
                        email=user_struct.email,
                        phone_number=user_struct.phone_number,
                        gender=user_struct.gender,
                        date_of_birth=user_struct.date_of_birth)

        return self.user_repo.create_user(new_user)

    async def update_user(self, user_id: int, update_fields: Dict) -> User:
        logger.info(f"Updating user with id {user_id}")
        return self.user_repo.update_user(user_id, update_fields)

    async def delete_user(self, user: User) -> None:
        logger.info(f"Deleting user with id {user.id}")
        return self.user_repo.delete_user(user)

    async def get_user(self, user_id: int) -> User:
        logger.info(f"Fetching user with id {user_id}")
        return self.user_repo.get_user(user_id)

    async def get_user_by_email(self, email: str) -> User:
        logger.info(f"[+] Fetching user with Email ---> {email}")
        return self.user_repo.get_user_by_email(email)