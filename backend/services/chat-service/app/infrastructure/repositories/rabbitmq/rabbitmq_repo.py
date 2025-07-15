from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.models.fitplan_chat_model import User, Coach, Admin

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