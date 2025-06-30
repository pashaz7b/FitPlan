from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.domain.schemas.coach_schema import (
    CoachRegisterSchema,
    CoachRegisterResponseSchema,
    VerifyOTPSchema,
    VerifyOTPResponseSchema,
    ResendOTPSchema,
    ResendOTPResponseSchema,
    CoachRegisterWithPhoneSchema,
    CoachRegisterWithPhoneResponseSchema,
    VerifyOTPPhoneSchema,
    VerifyOTPPhoneResponseSchema,
    ResendOTPPhoneSchema,
    ResendOTPPhoneResponseSchema,
    CoachRegisterWithPhoneFinalSchema,
    CoachRegisterWithPhoneFinalResponseSchema
)

from app.subservices.coach_subservice import CoachSubService
from app.subservices.user_duplicates_subservice import UserDuplicatesSubService
from app.subservices.auth.otp_subservice import OTPSubservice
from app.subservices.baseconfig import BaseService
from app.validators.regex_checker import RegexChecker

from app.mainservices.coach_otp_oken.coach_otp_token import CoachOtpToken


class CoachRegisterMainService(BaseService):
    def __init__(self,
                 coach_subservice: Annotated[CoachSubService, Depends()],
                 otp_subservice: Annotated[OTPSubservice, Depends()],
                 user_duplicates_subservice: Annotated[UserDuplicatesSubService, Depends()],
                 coach_otp_token: Annotated[CoachOtpToken, Depends()],
                 ) -> None:
        super().__init__()
        self.coach_subservice = coach_subservice
        self.otp_subservice = otp_subservice
        self.user_duplicates_subservice = user_duplicates_subservice
        self.coach_otp_token = coach_otp_token

    async def check_existence(self, coach):
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

    # ********************************************************************************************************

    async def check_phone_number_existence(self, coach_phone_schema: CoachRegisterWithPhoneSchema):
        existing_phone_number = await self.user_duplicates_subservice.get_user_by_phone_number(
            coach_phone_schema.phone_number)

        if existing_phone_number:
            logger.error(f"[-] Coach Phone Number ---> {coach_phone_schema.phone_number} Already Exists!!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="[-] A User With This Phone Number Already Exists!!"
            )

        logger.info(f"[...] Sending OTP For Phone Number ---> {coach_phone_schema.phone_number}")
        otp = self.otp_subservice.send_otp_to_phone(coach_phone_schema.phone_number)

        response = CoachRegisterWithPhoneResponseSchema(
            message="OTP Has Been Sent To Phone Number",
        )

        return response

    async def verify_otp_phone(self, verify_otp_phone_schema: VerifyOTPPhoneSchema):

        if not self.otp_subservice.verify_otp_phone(
                verify_otp_phone_schema.phone_number, verify_otp_phone_schema.OTP
        ):
            logger.error(f"[-] Invalid OTP For Phone ---> {verify_otp_phone_schema.phone_number}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP"
            )

        logger.info(f"[+] Coach with Phone ---> {verify_otp_phone_schema.phone_number} Verified")

        otp_token = await self.coach_otp_token.create_coach_otp_token(
            phone_number=verify_otp_phone_schema.phone_number,
            verified=True
        )

        response = JSONResponse(
            content=VerifyOTPPhoneResponseSchema(
                verified=True,
                message="Coach Verified Successfully",
                otp_token=otp_token
            ).dict()
        )

        response.set_cookie(
            key="otp_token",
            value=otp_token,
            httponly=True,
            secure=True,
            max_age=1800,
            samesite="Strict"
        )
        return response

        # return VerifyOTPPhoneResponseSchema(
        #     verified=True, message="Coach Verified Successfully"
        # )

    async def resend_otp_phone(self, resend_otp_phone_schema: ResendOTPPhoneSchema):

        existing_phone_number = await self.user_duplicates_subservice.get_user_by_phone_number(
            resend_otp_phone_schema.phone_number)

        if existing_phone_number:
            logger.error(f"[-] Coach Phone Number ---> {resend_otp_phone_schema.phone_number} Already Exists!!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="[-] A User With This Phone Number Already Exists!!"
            )

        if self.otp_subservice.check_exist_phone(resend_otp_phone_schema.phone_number):
            logger.error(f"[-] OTP For Phone ---> {resend_otp_phone_schema.phone_number} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="OTP Already Exists"
            )

        otp = self.otp_subservice.send_otp_to_phone(resend_otp_phone_schema.phone_number)

        logger.info(f"[+] OTP Resent To Phone ---> {resend_otp_phone_schema.phone_number}")
        return ResendOTPPhoneResponseSchema(
            phone_number=resend_otp_phone_schema.phone_number,
            message="OTP Sent To Phone",
        )

    async def register_coach_final(self, coach: CoachRegisterWithPhoneFinalSchema, otp_token: str):

        is_valid = await self.coach_otp_token.verify_coach_otp_token(
            phone_number=coach.phone_number,
            otp_token=otp_token
        )
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or unverified OTP token"
            )

        await self.check_existence(coach)
        new_coach = await self.coach_subservice.create_coach_final(coach)

        logger.info(f"[+] Coach With Email --> {coach.email} Created Successfully")
        response = JSONResponse(
            content=CoachRegisterWithPhoneFinalResponseSchema(
                message="[+] Coach Created Successfully"
            ).dict()
        )

        response.set_cookie(
            key="otp_token",
            value="",
            httponly=True,
            secure=True,
            max_age=0
        )
        return response
