from datetime import datetime, timedelta, timezone
from typing import Annotated
from loguru import logger
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.domain.models.user_model import User

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
from app.subservices.user_subservice import UserSubService


class PasswordManager(BaseService):
    def __init__(
            self,
            otp_subservice: Annotated[OTPSubservice, Depends()],
            user_subservice: Annotated[UserSubService, Depends()],
            hash_subservice: Annotated[HashService, Depends()]
    ) -> None:
        super().__init__()
        self.otp_subservice = otp_subservice
        self.user_subservice = user_subservice
        self.hash_subservice = hash_subservice

    async def forget_password(self, user: ForgetPasswordSchema) -> ForgetPasswordResponseSchema:
        logger.info(f"[...] Checking if user with email {user.email} exists")
        existing_user = await self.user_subservice.get_user_by_email(user.email)

        if not existing_user:
            logger.error(f"[-] User with email {user.email} does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email does not exist",
            )

        if not existing_user.is_verified:
            logger.error(f"[-] User with email {user.email} is not verified")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User email is not verified",
            )

        try:
            logger.info(f"[...] Sending Password_OTP to user with email {user.email}")
            self.otp_subservice.send_otp(email=user.email)
        except Exception as e:
            logger.error(f"[-] Failed to send Password_OTP to {user.email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send Password_OTP",
            )

        logger.info(f"[+] Password_OTP successfully sent to user with email {user.email}")
        message = f"Password_OTP has been sent to the email {user.email}"
        response = ForgetPasswordResponseSchema(email=user.email, message=message)
        return response

    async def verify_password_otp(self, verify_user_schema: VerifyPasswordOTPSchema):
        if not self.otp_subservice.verify_otp(
                verify_user_schema.email, verify_user_schema.OTP
        ):
            logger.error(f"[-] Invalid Password_OTP For Email ---> {verify_user_schema.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Password_OTP"
            )

        user = await self.user_subservice.get_user_by_email(
            verify_user_schema.email
        )

        # send Token
        token = await self.generate_token_with_limit(email=user.email)

        logger.info(f"[+] Token For Email ---> {verify_user_schema.email} Generated")
        return VerifyPasswordOTPResponseSchema(
            token= token ,message="Token Generated Successfully"
        )

    async def resend_password_otp(self, user: ResendPasswordOTPSchema) -> ResendPasswordOTPResponseSchema:
        logger.info(f"[...] Resending Password_OTP to user with email {user.email}")
        existing_user = await self.user_subservice.get_user_by_email(user.email)

        if not existing_user:
            logger.error(f"[-] User with email {user.email} does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email does not exist",
            )

        if self.otp_subservice.check_exist(user.email):
            logger.error(f"[-] Password_OTP For Email ---> {user.email} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Password_OTP Already Exists"
            )

        try:
            self.otp_subservice.send_otp(email=user.email)
        except Exception as e:
            logger.error(f"[-] Failed to resend Password_OTP to {user.email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to resend Password_OTP",
            )

        logger.info(f"[+] Password_OTP successfully resent to user with email {user.email}")
        message = f"Password_OTP has been resent to the email {user.email}"
        response = ResendPasswordOTPResponseSchema(email=user.email, message=message)
        return response

    async def generate_token_with_limit(self, email: str) -> str:
        logger.info(f"[...] Generating token for email {email}")
        expiration = datetime.now(timezone.utc) + timedelta(self.config.Password_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": email,
            "exp": expiration,
        }
        token = jwt.encode(payload, self.config.JWT_SECRET_KEY, algorithm=self.config.JWT_ALGORITHM)
        logger.info(f"[+] Token generated successfully for email {email}")
        return token

    async def change_password(self, change_password_schema: ChangePasswordSchema) -> ChangePasswordResponseSchema:
        try:
            payload = jwt.decode(
                change_password_schema.token, self.config.JWT_SECRET_KEY, algorithms=self.config.JWT_ALGORITHM
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

        logger.info(f"[...] Fetching user by email {email}")
        user = await self.user_subservice.get_user_by_email(email)
        if not user:
            logger.error(f"[-] User with email {email} does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if change_password_schema.new_password != change_password_schema.repeat_new_password:
            logger.error(f"[-] Password mismatch for user {email}. New password and repeat password do not match.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="The new password and repeat new password must match"
            )

        logger.info(f"[...] Updating password for user {email}")
        hashed_password = self.hash_subservice.hash_password(change_password_schema.new_password)
        await self.user_subservice.update_user_by_email(email, {"password": hashed_password})

        logger.info(f"[+] Password updated successfully for user {email}")
        return ChangePasswordResponseSchema(
            email=email, message="Password updated successfully"
        )
