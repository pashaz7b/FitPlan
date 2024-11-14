from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from loguru import logger

from app.domain.schemas.user_schema import (UserRegisterSchema,
                                            UserRegisterResponseSchema,
                                            UserDeleteSchema,
                                            VerifyOTPSchema,
                                            VerifyOTPResponseSchema,
                                            ResendOTPSchema,
                                            ResendOTPResponseSchema,
                                            UserLoginSchema,
                                            UserSchema)

from app.domain.schemas.token_schema import TokenSchema
from app.domain.models.user_model import User
from app.mainservices.register_mainservice import RegisterMainService
from app.infrastructure.repositories.user_repository import UserRepository
from app.mainservices.login_mainservice import AuthService, get_current_user

user_router = APIRouter()


@user_router.post("/signup", response_model=UserRegisterResponseSchema, status_code=status.HTTP_201_CREATED)
async def signup(user: UserRegisterSchema,
                 register_mainservice: Annotated[RegisterMainService, Depends()]) -> UserRegisterResponseSchema:
    logger.info(f"[...] Start Registering User")
    res = await register_mainservice.register_user(user)
    return res


@user_router.post("/verifyOTP", response_model=VerifyOTPResponseSchema, status_code=status.HTTP_200_OK)
async def verify_otp(verify_user_schema: VerifyOTPSchema,
                     register_service: Annotated[RegisterMainService, Depends()], ) -> VerifyOTPResponseSchema:
    logger.info(f"[...] Start Verifying OTP For User With Email ---> {verify_user_schema.email}")
    return await register_service.verify_user(verify_user_schema)


@user_router.post("/resendOTP", response_model=ResendOTPResponseSchema, status_code=status.HTTP_200_OK)
async def resend_otp(
        resend_otp_schema: ResendOTPSchema,
        register_service: Annotated[RegisterMainService, Depends()],
) -> ResendOTPResponseSchema:
    logger.info(f"[...] Start Resending OTP For User With Email {resend_otp_schema.email}")
    return await register_service.resend_otp(resend_otp_schema)


@user_router.post("/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: Annotated[AuthService, Depends()],
) -> TokenSchema:
    logger.info(f"[...] Logging In User with Email ---> {form_data.username}")
    return await auth_service.authenticate_user(
        UserLoginSchema(email=form_data.username, password=form_data.password)
    )



@user_router.get("/panel", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get_user(current_user: User = Depends(get_current_user)):
    logger.info(f"[...] Getting User with Email ---> {current_user.email}")
    return current_user