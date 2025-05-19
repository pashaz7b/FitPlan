import jdatetime

from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends

from app.domain.models.fitplan_chat_model import (User,
                                                  UserCoachChat,
                                                  UserCoachWith)

from app.domain.schemas.user_schema import (UserCreateChatSchema,
                                            UserCreateChatResponseSchema)
from app.infrastructure.repositories.user_repository import UserRepository
from app.subservices.baseconfig import BaseService


class UserSubService(BaseService):
    def __init__(self,
                 user_repo: Annotated[UserRepository, Depends()]
                 ) -> None:
        super().__init__()
        self.user_repo = user_repo

    async def create_user_chat(self, user_id, coach_id, user_create_chat_schema: UserCreateChatSchema):
        logger.info("[+] Creating Chat For User With Coach")

        user_coach_chat = UserCoachChat(
            user_id=user_id,
            coach_id=coach_id,
            content=user_create_chat_schema.content,
            sender_type="user",
            receiver_type="coach",
            date=jdatetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        return await self.user_repo.create_user_chat(user_coach_chat)

    async def get_user_coach(self, user_id: int):
        logger.info(f"Fetching user coach with user_id {user_id}")
        return await self.user_repo.get_user_coach(user_id)
