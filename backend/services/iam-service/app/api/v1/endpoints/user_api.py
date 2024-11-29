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

from app.domain.schemas.password_schema import (ForgetPasswordSchema,
                                                ForgetPasswordResponseSchema,
                                                ChangePasswordSchema,
                                                ChangePasswordResponseSchema,
                                                VerifyPasswordOTPSchema,
                                                VerifyPasswordOTPResponseSchema,
                                                ResendPasswordOTPSchema,
                                                ResendPasswordOTPResponseSchema)

from app.domain.schemas.token_schema import TokenSchema
from app.domain.models.user_model import User
from app.mainservices.user_register_mainservice import RegisterMainService
from app.infrastructure.repositories.user_repository import UserRepository
from app.mainservices.user_login_mainservice import AuthService, get_current_user
from app.mainservices.user_password_mainservice import PasswordManager

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




#****************************************************************************************************


@user_router.post("/forget_password", response_model=ForgetPasswordResponseSchema, status_code=status.HTTP_200_OK)
async def forget_password(
        user: ForgetPasswordSchema,
        password_service: Annotated[PasswordManager, Depends()],
):
    logger.info(f"[...] Start Sending Password_OTP For User With Email ---> {user.email}")
    return await password_service.forget_password(user)


@user_router.post("/verify_PasswordOTP", response_model=VerifyPasswordOTPResponseSchema, status_code=status.HTTP_200_OK)
async def verify_password_otp(verify_user_schema: VerifyPasswordOTPSchema,
                     password_service: Annotated[PasswordManager, Depends()], ) -> VerifyPasswordOTPResponseSchema:
    logger.info(f"[...] Start Verifying Password_OTP For User With Email ---> {verify_user_schema.email}")
    return await password_service.verify_password_otp(verify_user_schema)


@user_router.post("/resend_PasswordOTP", response_model=ResendPasswordOTPResponseSchema, status_code=status.HTTP_200_OK)
async def resend_password_otp(
        resend_passwordotp_schema: ResendPasswordOTPSchema,
        password_service: Annotated[PasswordManager, Depends()],
) -> ResendPasswordOTPResponseSchema:
    logger.info(f"[...] Start Resending Password_OTP For User With Email ---> {resend_passwordotp_schema.email}")
    return await password_service.resend_password_otp(resend_passwordotp_schema)



@user_router.put("/change_password", response_model=ChangePasswordResponseSchema, status_code=status.HTTP_200_OK)
async def change_password(
        change_password_schema: ChangePasswordSchema,
        password_service: Annotated[PasswordManager, Depends()],
) -> ChangePasswordResponseSchema:
    logger.info(f"[...] Start Resending Password_OTP For User")
    return await password_service.change_password(change_password_schema)




#****************************************************************************************************


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
