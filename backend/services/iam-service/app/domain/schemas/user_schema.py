from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, constr


class UserRegisterSchema(BaseModel):
    password: str
    user_name: str
    name: str
    email: EmailStr
    phone_number: constr(max_length=20)
    gender: Optional[constr(max_length=10)]
    date_of_birth: Optional[str]
    # image: Optional[str]
    # is_verified : bool


class UserRegisterResponseSchema(BaseModel):
    id: int
    # user_name: str
    # name: str
    # email: EmailStr
    # phone_number: Optional[str]
    # gender: Optional[str]
    # date_of_birth: Optional[str]
    # image: Optional[str]
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    message: str


class UserDeleteSchema(BaseModel):
    email: EmailStr
    password: str


# ********************************************************************************

class VerifyOTPSchema(BaseModel):
    email: EmailStr
    OTP: str


class VerifyOTPResponseSchema(BaseModel):
    verified: bool
    message: str


class ResendOTPSchema(BaseModel):
    email: EmailStr


class ResendOTPResponseSchema(BaseModel):
    email: str
    message: str


#**********************************************************************

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

#**********************************************************************

class UserSchema(BaseModel):
    id: int
    is_verified: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
