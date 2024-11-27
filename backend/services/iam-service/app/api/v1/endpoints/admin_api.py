from fastapi import Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from loguru import logger

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
from app.domain.schemas.token_schema import TokenSchema
from app.domain.models.admin_model import Admin
from app.mainservices.admin_register_mainservice import AdminRegisterMainService
from app.mainservices.admin_login_mainservice import AuthService, get_current_admin

admin_router = APIRouter()


@admin_router.post("/signup", response_model=AdminRegisterResponseSchema, status_code=status.HTTP_201_CREATED)
async def signup(admin: AdminRegisterSchema,
                 register_mainservice: Annotated[AdminRegisterMainService, Depends()]) -> AdminRegisterResponseSchema:
    logger.info(f"[...] Start Registering Admin")
    res = await register_mainservice.register_admin(admin)
    return res


@admin_router.post("/verifyOTP", response_model=VerifyOTPResponseSchema, status_code=status.HTTP_200_OK)
async def verify_otp(verify_admin_schema: VerifyOTPSchema,
                     register_service: Annotated[AdminRegisterMainService, Depends()]) -> VerifyOTPResponseSchema:
    logger.info(f"[...] Start Verifying OTP For Admin With Email ---> {verify_admin_schema.email}")
    return await register_service.verify_admin(verify_admin_schema)


@admin_router.post("/resendOTP", response_model=ResendOTPResponseSchema, status_code=status.HTTP_200_OK)
async def resend_otp(
        resend_otp_schema: ResendOTPSchema,
        register_service: Annotated[AdminRegisterMainService, Depends()],
) -> ResendOTPResponseSchema:
    logger.info(f"[...] Start Resending OTP For Admin With Email {resend_otp_schema.email}")
    return await register_service.resend_otp(resend_otp_schema)


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
