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
from app.subservices.admin_subservice import AdminSubService


class PasswordManager(BaseService):
    def __init__(
            self,
            otp_subservice: Annotated[OTPSubservice, Depends()],
            admin_subservice: Annotated[AdminSubService, Depends()],
            hash_subservice: Annotated[HashService, Depends()]
    ) -> None:
        super().__init__()
        self.otp_subservice = otp_subservice
        self.admin_subservice = admin_subservice
        self.hash_subservice = hash_subservice

    async def forget_password(self, admin: ForgetPasswordSchema) -> ForgetPasswordResponseSchema:
        logger.info(f"[...] Checking If Admin With Email ---> {admin.email} Exists")
        existing_admin= await self.admin_subservice.get_admin_by_email(admin.email)

        if not existing_admin:
            logger.error(f"[-] Admin With Email ---> {admin.email} Does Not Exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin With This Email Does Not Exist",
            )

        if not existing_admin.is_verified:
            logger.error(f"[-] Admin With Email ---> {admin.email} Is Not Verified")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin Email Is Not Verified",
            )

        try:
            logger.info(f"[...] Sending Password_OTP To Admin With Email ---> {admin.email}")
            self.otp_subservice.send_otp(email=admin.email)
        except Exception as e:
            logger.error(f"[-] Failed To Send Password_OTP To ---> {admin.email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed To Send Password_OTP",
            )

        logger.info(f"[+] Password_OTP Successfully Sent To Admin With Email ---> {admin.email}")
        message = f"Password_OTP Has Been Sent To The Email ---> {admin.email}"
        response = ForgetPasswordResponseSchema(email=admin.email, message=message)
        return response

    async def verify_password_otp(self, verify_admin_schema: VerifyPasswordOTPSchema):
        if not self.otp_subservice.verify_otp(
                verify_admin_schema.email, verify_admin_schema.OTP
        ):
            logger.error(f"[-] Invalid Password_OTP For Admin Email ---> {verify_admin_schema.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Password_OTP"
            )

        admin = await self.admin_subservice.get_admin_by_email(
            verify_admin_schema.email
        )

        # send Token
        token = await self.generate_token_with_limit(email=admin.email)

        logger.info(f"[+] Token For Admin Email ---> {verify_admin_schema.email} Generated")
        return VerifyPasswordOTPResponseSchema(
            token=token, message="Token Generated Successfully"
        )

    async def resend_password_otp(self, admin: ResendPasswordOTPSchema) -> ResendPasswordOTPResponseSchema:
        logger.info(f"[...] Resending Password_OTP To Admin With Email ---> {admin.email}")
        existing_admin = await self.admin_subservice.get_admin_by_email(admin.email)

        if not existing_admin:
            logger.error(f"[-] Admin With Email ---> {admin.email} Does Not Exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin With This Email Does Not Exist",
            )

        if self.otp_subservice.check_exist(admin.email):
            logger.error(f"[-] Password_OTP For Admin Email ---> {admin.email} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Password_OTP Already Exists"
            )

        try:
            self.otp_subservice.send_otp(email=admin.email)
        except Exception as e:
            logger.error(f"[-] Failed To Resend Password_OTP To ---> {admin.email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed To Resend Password_OTP",
            )

        logger.info(f"[+] Password_OTP Successfully Resent To Admin With Email ---> {admin.email}")
        message = f"Password_OTP Has Been Resent To The Email ---> {admin.email}"
        response = ResendPasswordOTPResponseSchema(email=admin.email, message=message)
        return response

    async def generate_token_with_limit(self, email: str) -> str:
        logger.info(f"[...] Generating Token For Admin Email ---> {email}")
        expiration = datetime.now(timezone.utc) + timedelta(self.config.Password_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": email,
            "exp": expiration,
        }
        token = jwt.encode(payload, self.config.JWT_SECRET_KEY, algorithm=self.config.JWT_ALGORITHM)
        logger.info(f"[+] Token Generated Successfully For Admin Email ---> {email}")
        return token

    async def change_password(self, token: str,
                              change_password_schema: ChangePasswordSchema) -> ChangePasswordResponseSchema:
        try:
            payload = jwt.decode(
                token, self.config.JWT_SECRET_KEY, algorithms=self.config.JWT_ALGORITHM
            )
            email = payload.get("sub")
        except jwt.ExpiredSignatureError:
            logger.error("[-] Token Has Expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            logger.error("[-] Invalid Token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        logger.info(f"[...] Fetching Admin By Email ---> {email}")
        admin = await self.admin_subservice.get_admin_by_email(email)
        if not admin:
            logger.error(f"[-] Admin With Email ---> {email} Does Not Exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Admin Not Found"
            )

        if change_password_schema.new_password != change_password_schema.repeat_new_password:
            logger.error(f"[-] Password Mismatch For Admin ---> {email}. New Password And Repeat Password Do Not Match.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="The New Password And Repeat New Password Must Match"
            )

        logger.info(f"[...] Updating Password For Admin ---> {email}")
        hashed_password = self.hash_subservice.hash_password(change_password_schema.new_password)
        await self.admin_subservice.update_admin_by_email(email, {"password": hashed_password})

        logger.info(f"[+] Password Updated Successfully For Admin ---> {email}")
        return ChangePasswordResponseSchema(
            email=email, message="Password Updated Successfully"
        )
