from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, constr


class CoachRegisterSchema(BaseModel):
    password: str
    user_name: str
    name: str
    email: str
    phone_number: constr(max_length=20)
    gender: constr(max_length=10)
    date_of_birth: str
    height: Optional[float]
    weight: Optional[float]
    specialization: Optional[str]
    biography: Optional[str]


class CoachRegisterResponseSchema(BaseModel):
    id: int
    user_name: str
    name: str
    email: EmailStr
    phone_number: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    message: str


# *****************************************************************


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


# *****************************************************************

class CoachLoginSchema(BaseModel):
    email: str
    password: str


class CoachSchema(BaseModel):
    id: int
    email: str
    is_verified: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


# *************************************************************************************

class GymVerificationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class CoachRegisterWithPhoneSchema(BaseModel):
    phone_number: constr(max_length=20)


class CoachRegisterWithPhoneResponseSchema(BaseModel):
    message: str


class VerifyOTPPhoneSchema(BaseModel):
    phone_number: constr(max_length=20)
    OTP: str


class VerifyOTPPhoneResponseSchema(BaseModel):
    verified: bool
    message: str
    otp_token: str | None = None


class ResendOTPPhoneSchema(BaseModel):
    phone_number: constr(max_length=20)


class ResendOTPPhoneResponseSchema(BaseModel):
    phone_number: constr(max_length=20)
    message: str


class CoachRegisterWithPhoneFinalSchema(BaseModel):
    password: str
    user_name: str
    name: str
    email: str
    phone_number: constr(max_length=20)
    gender: constr(max_length=10)
    date_of_birth: str
    height: Optional[float]
    weight: Optional[float]
    specialization: Optional[str]
    biography: Optional[str]
    is_verified: bool
    coaching_id: str
    coaching_card_image: str


class CoachRegisterWithPhoneFinalResponseSchema(BaseModel):
    message: str
