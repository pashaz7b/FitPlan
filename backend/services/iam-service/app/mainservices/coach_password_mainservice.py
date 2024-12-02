from datetime import datetime, timedelta, timezone
from typing import Annotated
from loguru import logger
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.domain.schemas.password_schema import (ForgetPasswordSchema,
                                                ForgetPasswordResponseSchema,
                                                ChangePasswordSchema,
                                                ChangePasswordResponseSchema,
                                                VerifyPasswordOTPSchema,
                                                VerifyPasswordOTPResponseSchema,
                                                ResendPasswordOTPSchema,
                                                ResendPasswordOTPResponseSchema)

from app.subservices.auth.hash_subservice import HashService
from app.subservices.auth.otp_subservice import OTPSubservice
from app.subservices.baseconfig import BaseService
from app.subservices.coach_subservice import CoachSubService


class PasswordManager(BaseService):
    def __init__(
            self,
            otp_subservice: Annotated[OTPSubservice, Depends()],
            coach_subservice: Annotated[CoachSubService, Depends()],
            hash_subservice: Annotated[HashService, Depends()]
    ) -> None:
        super().__init__()
        self.otp_subservice = otp_subservice
        self.coach_subservice = coach_subservice
        self.hash_subservice = hash_subservice

    async def forget_password(self, coach: ForgetPasswordSchema) -> ForgetPasswordResponseSchema:
        logger.info(f"[...] Checking if coach with email {coach.email} exists")
        existing_coach = await self.coach_subservice.get_coach_by_email(coach.email)

        if not existing_coach:
            logger.error(f"[-] Coach with email {coach.email} does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coach with this email does not exist",
            )

        if not existing_coach.is_verified:
            logger.error(f"[-] Coach with email {coach.email} is not verified")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coach email is not verified",
            )

        try:
            logger.info(f"[...] Sending Password_OTP to coach with email {coach.email}")
            self.otp_subservice.send_otp(email=coach.email)
        except Exception as e:
            logger.error(f"[-] Failed to send Password_OTP to {coach.email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send Password_OTP",
            )

        logger.info(f"[+] Password_OTP successfully sent to coach with email {coach.email}")
        message = f"Password_OTP has been sent to the email {coach.email}"
        response = ForgetPasswordResponseSchema(email=coach.email, message=message)
        return response

    async def verify_password_otp(self, verify_coach_schema: VerifyPasswordOTPSchema):
        if not self.otp_subservice.verify_otp(
                verify_coach_schema.email, verify_coach_schema.OTP
        ):
            logger.error(f"[-] Invalid Password_OTP For Coach Email ---> {verify_coach_schema.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Password_OTP"
            )

        coach = await self.coach_subservice.get_coach_by_email(
            verify_coach_schema.email
        )

        # send Token
        token = await self.generate_token_with_limit(email=coach.email)

        logger.info(f"[+] Token For Coach Email ---> {verify_coach_schema.email} Generated")
        return VerifyPasswordOTPResponseSchema(
            token=token, message="Token Generated Successfully"
        )

    async def resend_password_otp(self, coach: ResendPasswordOTPSchema) -> ResendPasswordOTPResponseSchema:
        logger.info(f"[...] Resending Password_OTP to coach with email {coach.email}")
        existing_coach = await self.coach_subservice.get_coach_by_email(coach.email)

        if not existing_coach:
            logger.error(f"[-] Coach with email {coach.email} does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coach with this email does not exist",
            )

        if self.otp_subservice.check_exist(coach.email):
            logger.error(f"[-] Password_OTP For Coach Email ---> {coach.email} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Password_OTP Already Exists"
            )

        try:
            self.otp_subservice.send_otp(email=coach.email)
        except Exception as e:
            logger.error(f"[-] Failed to resend Password_OTP to {coach.email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to resend Password_OTP",
            )

        logger.info(f"[+] Password_OTP successfully resent to coach with email {coach.email}")
        message = f"Password_OTP has been resent to the email {coach.email}"
        response = ResendPasswordOTPResponseSchema(email=coach.email, message=message)
        return response

    async def generate_token_with_limit(self, email: str) -> str:
        logger.info(f"[...] Generating token for coach email {email}")
        expiration = datetime.now(timezone.utc) + timedelta(self.config.Password_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": email,
            "exp": expiration,
        }
        token = jwt.encode(payload, self.config.JWT_SECRET_KEY, algorithm=self.config.JWT_ALGORITHM)
        logger.info(f"[+] Token generated successfully for coach email {email}")
        return token

    async def change_password(self, token: str,
                              change_password_schema: ChangePasswordSchema) -> ChangePasswordResponseSchema:
        try:
            payload = jwt.decode(
                token, self.config.JWT_SECRET_KEY, algorithms=self.config.JWT_ALGORITHM
            )
            email = payload.get("sub")
        except jwt.ExpiredSignatureError:
            logger.error("[-] Token has expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            logger.error("[-] Invalid token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        logger.info(f"[...] Fetching coach by email {email}")
        coach = await self.coach_subservice.get_coach_by_email(email)
        if not coach:
            logger.error(f"[-] Coach with email {email} does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Coach not found"
            )

        if change_password_schema.new_password != change_password_schema.repeat_new_password:
            logger.error(f"[-] Password mismatch for coach {email}. New password and repeat password do not match.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="The new password and repeat new password must match"
            )

        logger.info(f"[...] Updating password for coach {email}")
        hashed_password = self.hash_subservice.hash_password(change_password_schema.new_password)
        await self.coach_subservice.update_coach_by_email(email, {"password": hashed_password})

        logger.info(f"[+] Password updated successfully for coach {email}")
        return ChangePasswordResponseSchema(
            email=email, message="Password updated successfully"
        )
