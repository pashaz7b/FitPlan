from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc
# from sqlalchemy.orm import joinedload

from app.core.postgres_db.postgres_database import get_db
from app.domain.models.fitplan_chat_model import (User,
                                                  Coach,
                                                  UserCoachWith,
                                                  UserCoachChat)


class UserRepository:
    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]):
        self.db = db

    async def create_user_chat(self, user_coach_chat: UserCoachChat):
        self.db.add(user_coach_chat)
        await self.db.commit()
        await self.db.refresh(user_coach_chat)
        return user_coach_chat

    async def get_user_coach(self, user_id: int):
        logger.info(f"[+] Fetching Coach for User With Id ---> {user_id}")

        stmt = (
            select(Coach)
            .join(UserCoachWith, Coach.id == UserCoachWith.coach_id)
            .filter(UserCoachWith.user_id == user_id)
        )

        result = await self.db.execute(stmt)
        coach = result.scalars().first()

        return coach

    async def get_user_chat_messages(self, user_id: int, coach_id: int, limit: int = 50, offset: int = 0):
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
