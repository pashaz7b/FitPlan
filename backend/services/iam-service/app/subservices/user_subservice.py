from typing import Annotated, Dict
from uuid import UUID
from loguru import logger
from fastapi import Depends


from app.domain.models.user_model import User
from app.domain.schemas.user_schema import UserRegisterSchema
from app.infrastructure.repositories.user_repository import UserRepository


class UserSubService():
    def __init__(self):