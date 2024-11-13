from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, constr


class UserRegisterSchema(BaseModel):
    password: str
    user_name: str
    name: str
    email: EmailStr
    phone_number: Optional[constr(max_length=20)]
    gender: Optional[constr(max_length=10)]
    date_of_birth: Optional[str]
    # image: Optional[str]


class UserRegisterResponseSchema(BaseModel):
    id: int
    user_name: str
    name: str
    email: EmailStr
    phone_number: Optional[str]
    gender: Optional[str]
    date_of_birth: Optional[str]
    image: Optional[str]
    created_at: datetime
    updated_at: datetime

    # class Config:
    #     orm_mode = True
