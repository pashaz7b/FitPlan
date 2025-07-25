from fastapi import Depends, status, APIRouter, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from loguru import logger

from app.subservices.background_tasks.send_id_to_chatservice import SendIdToChat
from app.domain.schemas.admin_schema import (
    AdminRegisterSchema,
    AdminRegisterResponseSchema,
    VerifyOTPSchema,
    VerifyOTPResponseSchema,
    ResendOTPSchema,
    ResendOTPResponseSchema,
    AdminLoginSchema,
    AdminSchema
)

from app.domain.schemas.password_schema import (ForgetPasswordSchema,
                                                ForgetPasswordResponseSchema,
                                                ChangePasswordSchema,
                                                ChangePasswordResponseSchema,
                                                VerifyPasswordOTPSchema,
                                                VerifyPasswordOTPResponseSchema,
                                                ResendPasswordOTPSchema,
                                                ResendPasswordOTPResponseSchema)

from app.domain.schemas.token_schema import TokenSchema
from app.domain.models.admin_model import Admin
from app.mainservices.admin_register_mainservice import AdminRegisterMainService
from app.mainservices.admin_login_mainservice import AuthService, get_current_admin
from app.mainservices.admin_password_mainservice import PasswordManager

admin_router = APIRouter()


@admin_router.post("/signup", response_model=AdminRegisterResponseSchema, status_code=status.HTTP_201_CREATED)
async def signup(admin: AdminRegisterSchema,
                 register_mainservice: Annotated[AdminRegisterMainService, Depends()]) -> AdminRegisterResponseSchema:
    logger.info(f"[...] Start Registering Admin")
    res = await register_mainservice.register_admin(admin)
    return res


@admin_router.post("/verifyOTP", response_model=VerifyOTPResponseSchema, status_code=status.HTTP_200_OK)
async def verify_otp(verify_admin_schema: VerifyOTPSchema,
                     register_service: Annotated[AdminRegisterMainService, Depends()],
                     backgroundtasks: BackgroundTasks,
                     send_id_task: Annotated[SendIdToChat, Depends()]) -> VerifyOTPResponseSchema:
    logger.info(f"[...] Start Verifying OTP For Admin With Email ---> {verify_admin_schema.email}")
    response = await register_service.verify_admin(verify_admin_schema)
    if response.verified:
        backgroundtasks.add_task(send_id_task.send_admin_id, verify_admin_schema.email)
    return response

@admin_router.post("/resendOTP", response_model=ResendOTPResponseSchema, status_code=status.HTTP_200_OK)
async def resend_otp(
        resend_otp_schema: ResendOTPSchema,
        register_service: Annotated[AdminRegisterMainService, Depends()],
) -> ResendOTPResponseSchema:
    logger.info(f"[...] Start Resending OTP For Admin With Email {resend_otp_schema.email}")
    return await register_service.resend_otp(resend_otp_schema)


# ****************************************************************************************************


@admin_router.post("/forget_password", response_model=ForgetPasswordResponseSchema, status_code=status.HTTP_200_OK)
async def forget_password(
        admin: ForgetPasswordSchema,
        password_service: Annotated[PasswordManager, Depends()],
):
    logger.info(f"[...] Start Sending Password_OTP For Admin With Email ---> {admin.email}")
    return await password_service.forget_password(admin)


@admin_router.post("/verify_PasswordOTP", response_model=VerifyPasswordOTPResponseSchema,
                   status_code=status.HTTP_200_OK)
async def verify_password_otp(verify_admin_schema: VerifyPasswordOTPSchema,
                              password_service: Annotated[PasswordManager, Depends()],
                              ) -> VerifyPasswordOTPResponseSchema:
    logger.info(f"[...] Start Verifying Password_OTP For Admin With Email ---> {verify_admin_schema.email}")
    return await password_service.verify_password_otp(verify_admin_schema)


@admin_router.post("/resend_PasswordOTP", response_model=ResendPasswordOTPResponseSchema,
                   status_code=status.HTTP_200_OK)
async def resend_password_otp(
        resend_passwordotp_schema: ResendPasswordOTPSchema,
        password_service: Annotated[PasswordManager, Depends()],
) -> ResendPasswordOTPResponseSchema:
    logger.info(f"[...] Start Resending Password_OTP For Admin With Email ---> {resend_passwordotp_schema.email}")
    return await password_service.resend_password_otp(resend_passwordotp_schema)


@admin_router.put("/change_password/{token}", response_model=ChangePasswordResponseSchema,
                  status_code=status.HTTP_200_OK)
async def change_password(
        token: str,
        change_password_schema: ChangePasswordSchema,
        password_service: Annotated[PasswordManager, Depends()],
) -> ChangePasswordResponseSchema:
    logger.info(f"[...] Start Changing Password For Admin")
    return await password_service.change_password(token, change_password_schema)


# **********************************************************************************************


@admin_router.post("/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: Annotated[AuthService, Depends()],
) -> TokenSchema:
    logger.info(f"[...] Logging In Admin with Email ---> {form_data.username}")
    return await auth_service.authenticate_admin(
        AdminLoginSchema(email=form_data.username, password=form_data.password)
    )


@admin_router.get("/panel", response_model=AdminSchema, status_code=status.HTTP_200_OK)
async def get_admin(current_admin: Admin = Depends(get_current_admin)):
    logger.info(f"[...] Getting Admin with Email ---> {current_admin.email}")
    return current_admin
