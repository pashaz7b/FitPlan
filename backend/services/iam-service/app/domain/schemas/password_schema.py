from typing import Optional
from pydantic import BaseModel


class ForgetPasswordSchema(BaseModel):
    email: str


class ForgetPasswordResponseSchema(BaseModel):
    email: str
    message: str


class VerifyPasswordOTPSchema(BaseModel):
    email: str
    OTP: str


class VerifyPasswordOTPResponseSchema(BaseModel):
    token: str
    message: str


class ResendPasswordOTPSchema(BaseModel):
    email: str


class ResendPasswordOTPResponseSchema(BaseModel):
    email: str
    message: str


class ChangePasswordSchema(BaseModel):
    token: str
    new_password: str
    repeat_new_password: str


class ChangePasswordResponseSchema(BaseModel):
    email: str
    message: str
    token: Optional[str] = None
    new_password: Optional[str] = None
    repeat_new_password: Optional[str] = None
