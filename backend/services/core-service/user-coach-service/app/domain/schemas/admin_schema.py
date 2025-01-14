from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr


class GetAdminInfoSchema(BaseModel):
    password: Optional[str] = None
    user_name: str
    name: str
    email: str
    phone_number: constr(max_length=20)
    gender: Optional[constr(max_length=10)]
    date_of_birth: Optional[str]


class SetAdminInfoSchema(BaseModel):
    password: Optional[str]
    user_name: Optional[str]
    name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    gender: Optional[str]
    date_of_birth: Optional[str]


class GetAdminAllUsersSchema(BaseModel):
    user_id: Optional[int] = None
    user_password: Optional[str] = None
    user_user_name: Optional[str] = None
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    user_phone_number: Optional[str] = None
    user_gender: Optional[str] = None
    user_date_of_birth: Optional[str] = None
    user_height: Optional[float] = None
    user_weight: Optional[float] = None
    coach_id: Optional[int] = None
    coach_password: Optional[str] = None
    coach_user_name: Optional[str] = None
    coach_name: Optional[str] = None
    coach_email: Optional[str] = None
    coach_phone_number: Optional[str] = None
    coach_gender: Optional[str] = None
    coach_status: Optional[bool] = None
    coach_date_of_birth: Optional[str] = None
    coach_height: Optional[float] = None
    coach_weight: Optional[float] = None
    coach_specialization: Optional[str] = None
    coach_biography: Optional[str] = None
