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
