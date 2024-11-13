from typing import Annotated, Dict
from uuid import UUID
from loguru import logger
from fastapi import Depends

from app.domain.models.user_model import User
from app.domain.schemas.user_schema import UserRegisterSchema
from app.infrastructure.repositories.user_repository import UserRepository
from app.subservices.auth.hash_subservice import HashService


class UserSubService():
    def __init__(self,
                 user_repo: Annotated[UserRepository, Depends()],
                 hash_subservice: Annotated[HashService, Depends()]
                 ) -> None:
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