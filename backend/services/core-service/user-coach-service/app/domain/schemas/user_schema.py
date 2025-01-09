from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, constr


class GetUserInfoSchema(BaseModel):
    password: Optional[str] = None
    user_name: str
    name: str
    email: str
    phone_number: constr(max_length=20)
    gender: Optional[constr(max_length=10)]
    date_of_birth: Optional[str]
    height: Optional[float]
    weight: Optional[float]
    # waist: Optional[float]
    # injuries: Optional[str]
    # image: Optional[str]



class SetUserInfoSchema(BaseModel):
    password : Optional[str]
    user_name: Optional[str]
    name: Optional[str]
    email: Optional[str]
    phone_number: Optional [str]
    gender: Optional[str]
    date_of_birth: Optional[str]
    height: Optional[float]
    weight: Optional[float]


class GetUserTransactionsSchema(BaseModel):
    id: int
    amount: float
    reason: str
    status: str
    date: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None