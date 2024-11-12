from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from loguru import logger




user_router = APIRouter()


@user_router.post(
    "SignUp",

)