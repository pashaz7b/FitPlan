from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status

from app.domain.schemas.user_schema import (
    UserRegisterSchema,
    UserRegisterResponseSchema,
    VerifyOTPSchema,
    VerifyOTPResponseSchema,
    ResendOTPSchema,
    ResendOTPResponseSchema
)

from app.subservices.user_subservice import UserSubService
from app.subservices.user_duplicates_subservice import UserDuplicatesSubService
from app.subservices.auth.otp_subservice import OTPSubservice
from app.subservices.baseconfig import BaseService


class RegisterMainService(BaseService):
    def __init__(self, user_subservice: Annotated[UserSubService, Depends()],
                 otp_subservice: Annotated[OTPSubservice, Depends()],
                 user_duplicates_subservice: Annotated[UserDuplicatesSubService, Depends()]) -> None:
        super().__init__()
        self.user_subservice = user_subservice
        self.otp_subservice = otp_subservice
        self.user_duplicates_subservice = user_duplicates_subservice

    async def check_existence(self, user: UserRegisterSchema):
        existing_user_email = await self.user_duplicates_subservice.get_user_by_email(user.email)
        existing_user_phone_number = await self.user_duplicates_subservice.get_user_by_phone_number(user.phone_number)
        existing_user_name = await self.user_duplicates_subservice.get_user_by_user_name(user.user_name)
        # coach and admin user_duplicate

        if existing_user_email:
            logger.error(f"[-] User Email ---> {user.email} Already Exists!!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="[-] User With This Email Already Exists!!"
            )

        if existing_user_phone_number:
            logger.error(f"[-] User Phone Number ---> {user.phone_number} Already Exists!!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="[-] User With This Phone Number Already  Exists!!"
            )

        if existing_user_name:
            logger.error(f"[-] User Name ---> {user.user_name} Already Exists!!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="[-] User With This User Name Already Exists!!"
            )

    async def register_user(self, user: UserRegisterSchema) -> UserRegisterResponseSchema:
        await self.check_existence(user)

        # else:
        new_user = await self.user_subservice.create_user(user)
        otp = self.otp_subservice.send_otp(new_user.email)

        logger.info(f"[+] User With Email --> {user.email} Created Successfully")
        response = UserRegisterResponseSchema(
            id=new_user.id,
            user_name = new_user.user_name,
            name = new_user.name,
            email = new_user.email,
            is_verified=new_user.is_verified,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at,
            message="[+] User Created Successfully, OTP Sent To The Email"
        )
        return response

    async def verify_user(self, verify_user_schema: VerifyOTPSchema) -> VerifyOTPResponseSchema:
        if not self.otp_subservice.verify_otp(
                verify_user_schema.email, verify_user_schema.OTP
        ):
            logger.error(f"[-] Invalid OTP For Email ---> {verify_user_schema.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP"
            )

        user = await self.user_subservice.get_user_by_email(
            verify_user_schema.email
        )

        await self.user_subservice.update_user(user.id, {"is_verified": True})

        logger.info(f"[+] User with Email ---> {verify_user_schema.email} Verified")
        return VerifyOTPResponseSchema(
            verified=True, message="User Verified Successfully"
        )

    async def resend_otp(
            self, resend_otp_schema: ResendOTPSchema
    ) -> ResendOTPResponseSchema:
        existing_user = await self.user_subservice.get_user_by_email(
            resend_otp_schema.email
        )
        if not existing_user:
            logger.error(f"[-] User With Email {resend_otp_schema.email} Does Not Exist")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User Does Not Exist"
            )

        if existing_user.is_verified:
            logger.error(f"[-] User With Email ---> {resend_otp_schema.email} Already Verified")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User Already Verified"
            )

        if self.otp_subservice.check_exist(resend_otp_schema.email):
            logger.error(f"[-] OTP For Email ---> {resend_otp_schema.email} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="OTP Already Exists"
            )

        otp = self.otp_subservice.send_otp(resend_otp_schema.email)

        logger.info(f"[+] OTP Resent To Email ---> {resend_otp_schema.email}")
        return ResendOTPResponseSchema(
            email=resend_otp_schema.email,
            message="OTP Sent To Email",
        )
