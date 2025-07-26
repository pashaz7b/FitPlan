from typing import Dict
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.models.fitplan_chat_model import User, Coach, Admin, UserCoachWith


async def add_user(db: AsyncSession, user: User):
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def add_coach(db: AsyncSession, coach: Coach):
    db.add(coach)
    await db.commit()
    await db.refresh(coach)
    return coach


async def add_admin(db: AsyncSession, admin: Admin):
    db.add(admin)
    await db.commit()
    await db.refresh(admin)
    return admin


async def add_user_coach_with(db: AsyncSession, user_coach_with: UserCoachWith):
    db.add(user_coach_with)
    await db.commit()
    await db.refresh(user_coach_with)
    return user_coach_with


async def change_user_coach(db: AsyncSession, user_coach_with_dict: Dict):
    user_id = user_coach_with_dict.get("user_id")
    new_coach_id = user_coach_with_dict.get("new_coach_id")

    if not user_id or not new_coach_id:
        raise ValueError("user_id and new_coach_id are required.")

    # Find the record for the user
    result = await db.execute(select(UserCoachWith).where(UserCoachWith.user_id == user_id))
    user_coach = result.scalars().first()

    if not user_coach:
        raise ValueError(f"No record found for user_id={user_id}.")

    # Update the coach
    user_coach.coach_id = new_coach_id
    await db.commit()
    await db.refresh(user_coach)

    return user_coach
