from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status

from app.domain.schemas.coach_schema import (
    CoachRegisterSchema,
    CoachRegisterResponseSchema,
    VerifyOTPSchema,
    VerifyOTPResponseSchema,
    ResendOTPSchema,
    ResendOTPResponseSchema
)

from app.subservices.coach_subservice import CoachSubService
from app.subservices.user_duplicates_subservice import UserDuplicatesSubService
from app.subservices.auth.otp_subservice import OTPSubservice
from app.subservices.baseconfig import BaseService
from app.validators.regex_checker import RegexChecker


class CoachRegisterMainService(BaseService):
    def __init__(self,
                 coach_subservice: Annotated[CoachSubService, Depends()],
                 otp_subservice: Annotated[OTPSubservice, Depends()],
                 user_duplicates_subservice: Annotated[UserDuplicatesSubService, Depends()]) -> None:
        super().__init__()
        self.coach_subservice = coach_subservice
        self.otp_subservice = otp_subservice
        self.user_duplicates_subservice = user_duplicates_subservice

    async def check_existence(self, coach: CoachRegisterSchema):
        existing_email = await self.user_duplicates_subservice.get_user_by_email(coach.email)
        existing_phone_number = await self.user_duplicates_subservice.get_user_by_phone_number(coach.phone_number)
        existing_user_name = await self.user_duplicates_subservice.get_user_by_user_name(coach.user_name)

        if existing_email:
            logger.error(f"[-] Coach Email ---> {coach.email} Already Exists!!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="[-] A User With This Email Already Exists!!"
            )

        if existing_phone_number:
            logger.error(f"[-] Coach Phone Number ---> {coach.phone_number} Already Exists!!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="[-] A User With This Phone Number Already Exists!!"
            )

        if existing_user_name:
            logger.error(f"[-] Coach User Name ---> {coach.user_name} Already Exists!!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="[-] A User With This User Name Already Exists!!"
            )

    async def register_coach(self, coach: CoachRegisterSchema) -> CoachRegisterResponseSchema:

        if not RegexChecker.is_valid_email(coach.email):
            logger.error(f"[-] Invalid Email ---> {coach.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email"
            )

        await self.check_existence(coach)

        new_coach = await self.coach_subservice.create_coach(coach)
        otp = self.otp_subservice.send_otp(new_coach.email)

        logger.info(f"[+] Coach With Email --> {coach.email} Created Successfully")
        response = CoachRegisterResponseSchema(
            id=new_coach.id,
            user_name=coach.user_name,
            name=coach.name,
            email=coach.email,
            phone_number=coach.phone_number,
            is_verified=new_coach.is_verified,
            created_at=new_coach.created_at,
            updated_at=new_coach.updated_at,
            message="[+] Coach Created Successfully, OTP Sent To The Email"
        )
        return response

    async def verify_coach(self, verify_coach_schema: VerifyOTPSchema) -> VerifyOTPResponseSchema:
        if not self.otp_subservice.verify_otp(
                verify_coach_schema.email, verify_coach_schema.OTP
        ):
            logger.error(f"[-] Invalid OTP For Email ---> {verify_coach_schema.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP"
            )

        coach = await self.coach_subservice.get_coach_by_email(
            verify_coach_schema.email
        )

        await self.coach_subservice.update_coach(coach.id, {"is_verified": True})

        logger.info(f"[+] Coach with Email ---> {verify_coach_schema.email} Verified")
        return VerifyOTPResponseSchema(
            verified=True, message="Coach Verified Successfully"
        )

    async def resend_otp(self, resend_otp_schema: ResendOTPSchema) -> ResendOTPResponseSchema:
        existing_coach = await self.coach_subservice.get_coach_by_email(
            resend_otp_schema.email
        )
        if not existing_coach:
            logger.error(f"[-] Coach With Email {resend_otp_schema.email} Does Not Exist")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Coach Does Not Exist"
            )

        if existing_coach.is_verified:
            logger.error(f"[-] Coach With Email ---> {resend_otp_schema.email} Already Verified")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Coach Already Verified"
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
