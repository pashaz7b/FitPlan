from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status

from app.domain.schemas.admin_schema import (GetAdminInfoSchema,
                                             SetAdminInfoSchema)

from app.subservices.admin_subservice import AdminSubService
from app.subservices.user_duplicates_subservice import UserDuplicatesSubService
from app.subservices.baseconfig import BaseService
from app.subservices.auth.hash_subservice import HashService


class AdminMainService(BaseService):
    def __init__(self,
                 admin_subservice: Annotated[AdminSubService, Depends()],
                 user_duplicates_subservice: Annotated[UserDuplicatesSubService, Depends()],
                 hash_subservice: Annotated[HashService, Depends()]
                 ) -> None:
        super().__init__()
        self.admin_subservice = admin_subservice
        self.user_duplicates_subservice = user_duplicates_subservice
        self.hash_subservice = hash_subservice

    async def check_email_existence(self, email: str):
        existing_user_email = await self.user_duplicates_subservice.get_user_by_email(email)
        if existing_user_email:
            logger.error(f"[-] User Email ---> {email} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User With This Email Already Exists"
            )

    async def check_phone_number_existence(self, phone_number: str):
        existing_user_phone_number = await self.user_duplicates_subservice.get_user_by_phone_number(phone_number)
        if existing_user_phone_number:
            logger.error(f"[-] User Phone Number ---> {phone_number} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User With This Phone Number Already Exists"
            )

    async def check_user_name_existence(self, user_name: str):
        existing_user_name = await self.user_duplicates_subservice.get_user_by_user_name(user_name)
        if existing_user_name:
            logger.error(f"[-] User Name ---> {user_name} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User With This User Name Already Exists"
            )

    async def get_admin_info(self, admin_id: int) -> GetAdminInfoSchema:
        admin = await self.admin_subservice.get_admin(admin_id)

        empty_password = ""
        return GetAdminInfoSchema(
            password=empty_password,
            user_name=admin.user_name,
            name=admin.name,
            email=admin.email,
            phone_number=admin.phone_number,
            gender=admin.gender,
            date_of_birth=admin.date_of_birth,
        )
