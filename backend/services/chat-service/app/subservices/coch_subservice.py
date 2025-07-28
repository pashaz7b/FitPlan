import jdatetime

from typing import Annotated
from loguru import logger
from fastapi import Depends
from app.domain.models.fitplan_chat_model import (User,
                                                  Coach,
                                                  UserCoachChat,
                                                  UserCoachWith)

from app.domain.schemas.coach_schema import (CoachCreateChatSchema,
                                             CoachCreateChatResponseSchema)
from app.infrastructure.repositories.coach_repository import CoachRepository
from app.subservices.baseconfig import BaseService


class CoachSubService(BaseService):
    def __init__(self,
                 coach_repo: Annotated[CoachRepository, Depends()]
                 ) -> None:
        super().__init__()
        self.coach_repo = coach_repo

    async def create_coach_chat(self, coach_id, user_id,coach_create_chat_schema: CoachCreateChatSchema):
        logger.info("[+] Creating Chat For Coach With User")

        coach_user_chat = UserCoachChat(
            user_id=user_id,
            coach_id=coach_id,
            content=coach_create_chat_schema.content,
            sender_type="coach",
            receiver_type="user",
            date=jdatetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        return await self.coach_repo.create_coach_chat(coach_user_chat)

    # async def get_user_coach(self, user_id: int):
    #     logger.info(f"Fetching user coach with user_id {user_id}")
    #     return await self.user_repo.get_user_coach(user_id)

    async def get_coach_chat_messages(self, user_id: int, coach_id: int, limit: int = 50, offset: int = 0):
        logger.info(f"[+] getting user coach chat for user with id {user_id}")
        return await self.coach_repo.get_coach_chat_messages(user_id, coach_id, limit, offset)
