from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from loguru import logger

from app.domain.schemas.coach_schema import (CoachRegisterSchema,
                                             CoachRegisterResponseSchema,
                                             VerifyOTPSchema,
                                             VerifyOTPResponseSchema,
                                             ResendOTPSchema,
                                             ResendOTPResponseSchema,
                                             CoachLoginSchema,
                                             CoachSchema)
from app.domain.schemas.password_schema import (ForgetPasswordSchema,
                                                ForgetPasswordResponseSchema,
                                                ChangePasswordSchema,
                                                ChangePasswordResponseSchema,
                                                VerifyPasswordOTPSchema,
                                                VerifyPasswordOTPResponseSchema,
                                                ResendPasswordOTPSchema,
                                                ResendPasswordOTPResponseSchema)
from app.domain.schemas.token_schema import TokenSchema
from app.domain.models.coach_model import Coach
from app.mainservices.coach_register_mainservice import CoachRegisterMainService
from app.mainservices.coach_login_mainservice import AuthService, get_current_coach
from app.mainservices.coach_password_mainservice import PasswordManager

coach_router = APIRouter()


@coach_router.post("/signup", response_model=CoachRegisterResponseSchema, status_code=status.HTTP_201_CREATED)
async def signup(coach: CoachRegisterSchema,
                 register_mainservice: Annotated[CoachRegisterMainService, Depends()]) -> CoachRegisterResponseSchema:
    logger.info(f"[...] Start Registering Coach")
    res = await register_mainservice.register_coach(coach)
    return res


@coach_router.post("/verifyOTP", response_model=VerifyOTPResponseSchema, status_code=status.HTTP_200_OK)
async def verify_otp(verify_coach_schema: VerifyOTPSchema,
                     register_service: Annotated[CoachRegisterMainService, Depends()]) -> VerifyOTPResponseSchema:
    logger.info(f"[...] Start Verifying OTP For Coach With Email ---> {verify_coach_schema.email}")
    return await register_service.verify_coach(verify_coach_schema)


@coach_router.post("/resendOTP", response_model=ResendOTPResponseSchema, status_code=status.HTTP_200_OK)
async def resend_otp(
        resend_otp_schema: ResendOTPSchema,
        register_service: Annotated[CoachRegisterMainService, Depends()],
) -> ResendOTPResponseSchema:
    logger.info(f"[...] Start Resending OTP For Coach With Email {resend_otp_schema.email}")
    return await register_service.resend_otp(resend_otp_schema)


# ****************************************************************************************************


@coach_router.post("/forget_password", response_model=ForgetPasswordResponseSchema, status_code=status.HTTP_200_OK)
async def forget_password(
        coach: ForgetPasswordSchema,
        password_service: Annotated[PasswordManager, Depends()],
):
    logger.info(f"[...] Start Sending Password_OTP For Coach With Email ---> {coach.email}")
    return await password_service.forget_password(coach)


@coach_router.post("/verify_PasswordOTP", response_model=VerifyPasswordOTPResponseSchema,
                   status_code=status.HTTP_200_OK)
async def verify_password_otp(verify_coach_schema: VerifyPasswordOTPSchema,
                              password_service: Annotated[PasswordManager, Depends()],
                              ) -> VerifyPasswordOTPResponseSchema:
    logger.info(f"[...] Start Verifying Password_OTP For Coach With Email ---> {verify_coach_schema.email}")
    return await password_service.verify_password_otp(verify_coach_schema)


@coach_router.post("/resend_PasswordOTP", response_model=ResendPasswordOTPResponseSchema,
                   status_code=status.HTTP_200_OK)
async def resend_password_otp(
        resend_passwordotp_schema: ResendPasswordOTPSchema,
        password_service: Annotated[PasswordManager, Depends()],
) -> ResendPasswordOTPResponseSchema:
    logger.info(f"[...] Start Resending Password_OTP For Coach With Email ---> {resend_passwordotp_schema.email}")
    return await password_service.resend_password_otp(resend_passwordotp_schema)


@coach_router.put("/change_password/{token}", response_model=ChangePasswordResponseSchema,
                  status_code=status.HTTP_200_OK)
async def change_password(
        token: str,
        change_password_schema: ChangePasswordSchema,
        password_service: Annotated[PasswordManager, Depends()],
) -> ChangePasswordResponseSchema:
    logger.info(f"[...] Start Changing Password For Coach")
    return await password_service.change_password(token, change_password_schema)


# ****************************************************************************************************
@coach_router.post("/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: Annotated[AuthService, Depends()],
) -> TokenSchema:
    logger.info(f"[...] Logging In Coach with Email ---> {form_data.username}")
    return await auth_service.authenticate_coach(
        CoachLoginSchema(email=form_data.username, password=form_data.password)
    )


@coach_router.get("/panel", response_model=CoachSchema, status_code=status.HTTP_200_OK)
async def get_coach(current_coach: Coach = Depends(get_current_coach)):
    logger.info(f"[...] Getting Coach with Email ---> {current_coach.email}")
    return current_coach
