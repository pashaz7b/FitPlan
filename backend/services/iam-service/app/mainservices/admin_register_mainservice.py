from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status

from app.domain.schemas.admin_schema import (
    AdminRegisterSchema,
    AdminRegisterResponseSchema,
    VerifyOTPSchema,
    VerifyOTPResponseSchema,
    ResendOTPSchema,
    ResendOTPResponseSchema
)

from app.subservices.admin_subservice import AdminSubService
from app.subservices.user_duplicates_subservice import UserDuplicatesSubService
from app.subservices.auth.otp_subservice import OTPSubservice
from app.subservices.baseconfig import BaseService
from app.validators.regex_checker import RegexChecker


class AdminRegisterMainService(BaseService):
    def __init__(self,
                 admin_subservice: Annotated[AdminSubService, Depends()],
                 otp_subservice: Annotated[OTPSubservice, Depends()],
                 user_duplicates_subservice: Annotated[UserDuplicatesSubService, Depends()]) -> None:
        super().__init__()
        self.admin_subservice = admin_subservice
        self.otp_subservice = otp_subservice
        self.user_duplicates_subservice = user_duplicates_subservice

    async def check_existence(self, admin: AdminRegisterSchema):
        existing_email = await self.user_duplicates_subservice.get_user_by_email(admin.email)
        existing_phone_number = await self.user_duplicates_subservice.get_user_by_phone_number(admin.phone_number)
        existing_user_name = await self.user_duplicates_subservice.get_user_by_user_name(admin.user_name)

        if existing_email:
            logger.error(f"[-] Admin Email ---> {admin.email} Already Exists!!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="[-] A User With This Email Already Exists!!"
            )

        if existing_phone_number:
            logger.error(f"[-] Admin Phone Number ---> {admin.phone_number} Already Exists!!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="[-] A User With This Phone Number Already Exists!!"
            )

        if existing_user_name:
            logger.error(f"[-] Admin User Name ---> {admin.user_name} Already Exists!!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="[-] A User With This User Name Already Exists!!"
            )

    async def register_admin(self, admin: AdminRegisterSchema) -> AdminRegisterResponseSchema:

        if not RegexChecker.is_valid_email(admin.email):
            logger.error(f"[-] Invalid Email ---> {admin.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email"
            )

        await self.check_existence(admin)

        new_admin = await self.admin_subservice.create_admin(admin)
        otp = self.otp_subservice.send_otp(new_admin.email)

        logger.info(f"[+] Admin With Email --> {admin.email} Created Successfully")
        response = AdminRegisterResponseSchema(
            id=new_admin.id,
            user_name=admin.user_name,
            name=admin.name,
            email=admin.email,
            phone_number=admin.phone_number,
            is_verified=new_admin.is_verified,
            created_at=new_admin.created_at,
            updated_at=new_admin.updated_at,
            message="[+] Admin Created Successfully, OTP Sent To The Email"
        )
        return response

    async def verify_admin(self, verify_admin_schema: VerifyOTPSchema) -> VerifyOTPResponseSchema:
        if not self.otp_subservice.verify_otp(
                verify_admin_schema.email, verify_admin_schema.OTP
        ):
            logger.error(f"[-] Invalid OTP For Email ---> {verify_admin_schema.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP"
            )

        admin = await self.admin_subservice.get_admin_by_email(
            verify_admin_schema.email
        )

        await self.admin_subservice.update_admin(admin.id, {"is_verified": True})

        logger.info(f"[+] Admin with Email ---> {verify_admin_schema.email} Verified")
        return VerifyOTPResponseSchema(
            verified=True, message="Admin Verified Successfully"
        )

    async def resend_otp(self, resend_otp_schema: ResendOTPSchema) -> ResendOTPResponseSchema:
        existing_admin = await self.admin_subservice.get_admin_by_email(
            resend_otp_schema.email
        )
        if not existing_admin:
            logger.error(f"[-] Admin With Email {resend_otp_schema.email} Does Not Exist")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Admin Does Not Exist"
            )

        if existing_admin.is_verified:
            logger.error(f"[-] Admin With Email ---> {resend_otp_schema.email} Already Verified")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Admin Already Verified"
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
