from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user_coach_chat = relationship("UserCoachChat", back_populates="user")
    user_coach_with = relationship("UserCoachWith", back_populates="user")

class Coach(Base):
    __tablename__ = "coach"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user_coach_chat = relationship("UserCoachChat", back_populates="coach")
    user_coach_with = relationship("UserCoachWith", back_populates="coach")


class UserCoachChat(Base):
    __tablename__ = "user_coach_chat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    coach_id = Column(Integer, ForeignKey("coach.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    sender_type = Column(String(10), nullable=False)
    receiver_type = Column(String(10), nullable=False)
    date = Column(String(55))
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="user_coach_chat")
    coach = relationship("Coach", back_populates="user_coach_chat")


class UserCoachWith(Base):
    __tablename__ = "user_coach_with"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    coach_id = Column(Integer, ForeignKey("coach.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="user_coach_with")
    coach = relationship("Coach", back_populates="user_coach_with")
