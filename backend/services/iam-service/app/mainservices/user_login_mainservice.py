from datetime import datetime, timedelta, timezone
from typing import Annotated
from loguru import logger
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.domain.models.user_model import User
from app.domain.schemas.token_schema import TokenSchema
from app.domain.schemas.user_schema import (UserLoginSchema,
                                            UserForgetPasswordSchema,
                                            UserForgetPasswordResponseSchema)
from app.subservices.auth.hash_subservice import HashService
from app.subservices.auth.otp_subservice import OTPSubservice
from app.subservices.baseconfig import BaseService
from app.subservices.user_subservice import UserSubService

user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")


class AuthService(BaseService):
    def __init__(
            self,
            hash_service: Annotated[HashService, Depends()],
            user_service: Annotated[UserSubService, Depends()],
    ) -> None:
        super().__init__()
        self.user_service = user_service
        self.hash_service = hash_service

    async def authenticate_user(self, user: UserLoginSchema) -> TokenSchema:
        existing_user = await self.user_service.get_user_by_email(
            user.email
        )
        logger.info(f"[...] Authenticating User With Email ---> {user.email}")

        if not existing_user:
            logger.error(f"[-] User With Email ---> {user.email} Does Not Exist")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User Does Not Exist"
            )

        if not existing_user.is_verified:
            logger.error(f"[-] User with Email {user.email} Is Not Verified")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User Is Not Verified"
            )

        if not self.hash_service.verify_password(
                user.password, existing_user.password
        ):
            logger.error(f"[-] Invalid Password For User With Email ---> {user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self.create_access_token(data={"sub": str(existing_user.id)})

        logger.info(f"[+] User With Email ---> {user.email} Authenticated Successfully")
        return TokenSchema(access_token=access_token, token_type="bearer")

    def create_access_token(self, data: dict) -> str:
        logger.info("Creating Access Token")
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            self.config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.config.JWT_SECRET_KEY, algorithm=self.config.JWT_ALGORITHM
        )
        return encoded_jwt


class PasswordManager:
    def __init__(
            self,
            otp_subservice: Annotated[OTPSubservice, Depends()],
            user_service: Annotated[UserSubService, Depends()],
    ) -> None:
        self.otp_subservice = otp_subservice
        self.user_service = user_service

    async def forget_password(self, user: UserForgetPasswordSchema) -> UserForgetPasswordResponseSchema:
        logger.info(f"[...] Checking if user with email {user.email} exists")
        existing_user = await self.user_service.get_user_by_email(user.email)

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
        response = UserForgetPasswordResponseSchema(email=user.email, message=message)
        return response


async def get_current_user(
        token: Annotated[str, Depends(user_oauth2_scheme)],
        user_service: Annotated[UserSubService, Depends()],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could Not Validate Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logger.info(f"[...] Validating Token {token}")
    try:
        payload = jwt.decode(
            token,
            user_service.config.JWT_SECRET_KEY,
            algorithms=[user_service.config.JWT_ALGORITHM],
        )
        user_id: int = payload.get("sub")
        user = await user_service.get_user(user_id)
        if user_id is None:
            logger.error("[-] Could Not Validate Credentials")
            raise credentials_exception
    except jwt.PyJWTError:
        logger.error("[-] Error Decoding Token")
        raise credentials_exception

    logger.info(f"[+] User With Id ---> {user_id} Validated Successfully")
    return user


# async def forget_password(
#         user: UserForgetPasswordSchema,
#         otp_subservice: Annotated[OTPSubservice, Depends()],
#         user_service: Annotated[UserSubService, Depends()],
# ):
#     logger.info(f"[...] Checking if user with email {user.email} exists")
#     existing_user = await user_service.get_user_by_email(user.email)
#
#     if not existing_user:
#         logger.error(f"[-] User with email {user.email} does not exist")
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User with this email does not exist",
#         )
#
#     if not existing_user.is_verified:
#         logger.error(f"[-] User with email {user.email} is not verified")
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User email is not verified",
#         )
#
#     try:
#         logger.info(f"[...] Sending Password_OTP to user with email {user.email}")
#         otp_subservice.send_otp(email=user.email)
#     except Exception as e:
#         logger.error(f"[-] Failed to send Password_OTP to {user.email}: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to send Password_OTP",
#         )
#
#     logger.info(f"[+] Password_OTP successfully sent to user with email {user.email}")
#     message = f" Password_OTP has been sent to the email {user.email}"
#     response = UserForgetPasswordResponseSchema(email=user.email, message=message)
#     return response
