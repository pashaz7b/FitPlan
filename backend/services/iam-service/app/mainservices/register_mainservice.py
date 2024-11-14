from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status

from app.domain.schemas.user_schema import (
    UserRegisterSchema,
    UserRegisterResponseSchema
)

from app.subservices.user_subservice import UserSubService
from app.subservices.auth.opt_subservice import OTPSubservice
from app.subservices.baseconfig import BaseService


class RegisterMainService(BaseService):
    def __init__(self, user_subservice: Annotated[UserSubService, Depends()],
                 otp_subservice: Annotated[OTPSubservice, Depends()]) -> None:
        super().__init__()
        self.user_subservice = user_subservice
        self.otp_subservice = otp_subservice

    async def check_existence(self, user: UserRegisterSchema):
        existing_user_name = ""
        existing_user_email = await self.user_subservice.get_user_by_email(user.email)
        existing_user_phone_number = ""
        # coach and admin user_duplicate

        if existing_user_email:
            logger.error(f"[-] User Email ---> {user.email} Already Exists!!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="[-] User Already Exists!!"
            )

    async def register_user(self, user: UserRegisterSchema) -> UserRegisterResponseSchema:
        await self.check_existence(user)

        # else:
        new_user = await self.user_subservice.create_user(user)
        otp = self.otp_subservice.send_otp(new_user.email)

        logger.info(f"[+] User With Email --> {user.email} Created Successfully")
        response = UserRegisterResponseSchema(
            id=new_user.id,
            is_verified=new_user.is_verified,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at,
            message="[+] User Created Successfully, OTP Sent To The Email"
        )
        return response
