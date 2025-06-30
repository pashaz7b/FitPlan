from typing import Annotated
# from loguru import logger
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.postgres_db.postgres_database import get_db
from app.domain.models.fitplan_chat_model import (User,
                                                  Coach,
                                                  UserCoachWith,
                                                  UserCoachChat)


class CoachRepository:
    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]):
        self.db = db

    async def create_coach_chat(self, user_coach_chat: UserCoachChat):
        self.db.add(user_coach_chat)
        await self.db.commit()
        await self.db.refresh(user_coach_chat)
        return user_coach_chat

    # async def get_coach_user(self, user_id: int, coach_id: int):
    #     stmt = (
    #         select(Coach)
    #         .filter(Coach.id == coach_id)
    #         .join(UserCoachWith, Coach.id == UserCoachWith.coach_id)
    #         .filter(UserCoachWith.user_id == user_id)
    #     )
    #
    #     result = await self.db.execute(stmt)
    #     coach_user = result.scalars().first()
    #
    #     return coach_user

    async def get_coach_chat_messages(self, user_id: int, coach_id: int, limit: int = 50, offset: int = 0):
        stmt = (
            select(UserCoachChat)
            .where(
                (UserCoachChat.user_id == user_id) &
                (UserCoachChat.coach_id == coach_id)
            )
            # .order_by(desc(UserCoachChat.created_at))
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
