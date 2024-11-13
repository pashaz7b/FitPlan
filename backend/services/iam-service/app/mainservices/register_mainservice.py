from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status

from app.domain.schemas.user_schema import (
    UserRegisterSchema,
    UserRegisterResponseSchema
)

from app.subservices.user_subservice import UserSubService
from app.subservices.auth.opt_subservice import OTPSubservice
from app.subservices.baseconfig import BaseService


class RegisterMainService(BaseService):
    def __init__(self,
                 user_subservice: Annotated[UserSubService, Depends()],
                 otp_subservice: Annotated[OTPSubservice, Depends()]
                 ) -> None:
        super().__init__()
        self.user_subservice = user_subservice
        self.otp_subservice = otp_subservice

    async def register_user(self, user: UserRegisterSchema):
        new_user = await self.user_subservice.create_user(user)
        otp = self.otp_subservice.send_otp(new_user.email)
        # response =  UserRegisterResponseSchema(user)
        return user
