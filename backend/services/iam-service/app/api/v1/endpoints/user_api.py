from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from loguru import logger

from app.domain.schemas.user_schema import (UserRegisterSchema, UserRegisterResponseSchema, UserDeleteSchema)
from app.mainservices.register_mainservice import RegisterMainService
from app.infrastructure.repositories.user_repository import UserRepository

user_router = APIRouter()


@user_router.post(
    "/signup",
    response_model=UserRegisterResponseSchema,
    status_code=status.HTTP_201_CREATED
)
async def signup(
        user: UserRegisterSchema, register_mainservice: Annotated[RegisterMainService, Depends()]
):
    res = await register_mainservice.register_user(user)
    return res