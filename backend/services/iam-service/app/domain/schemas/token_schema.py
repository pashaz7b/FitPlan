from typing import Optional
from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class PasswordTokenSchema(BaseModel):
    password_token: str
