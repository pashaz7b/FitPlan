# from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func, Sequence, ForeignKey, Numeric, Boolean
# from sqlalchemy.orm import relationship
#
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
#
# class Coach(Base):
#     __tablename__ = "coach"
#
#     id = Column(Integer, Sequence("coach_id_seq"), primary_key=True)
#     password = Column(String(255), nullable=False)
#     user_name = Column(String(255), unique=True, nullable=False)
#     name = Column(String(255), nullable=False)
#     email = Column(String(255), unique=True, nullable=False)
#     phone_number = Column(String(20), unique=True, nullable=False)
#     gender = Column(String(10))
#     status = Column(Boolean, default=False)
#     date_of_birth = Column(String(15))
#     image = Column(Text)
#     created_at = Column(TIMESTAMP, server_default=func.now())
#     updated_at = Column(TIMESTAMP, server_default=func.now())
#     is_verified = Column(Boolean, default=False)
#
#     metrics = relationship("CoachMetrics", back_populates="coach", uselist=False)
#
#
# class CoachMetrics(Base):
#     __tablename__ = 'coach_metrics'
#
#     id = Column(Integer, primary_key=True, index=True)
#     coach_id = Column(Integer, ForeignKey('coach.id', ondelete='CASCADE'), unique=True)
#     height = Column(Numeric(5, 2))
#     weight = Column(Numeric(5, 2))
#     specialization = Column(String(255))
#     biography = Column(Text)
#     created_at = Column(TIMESTAMP, default=func.now())
#     updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
#
#     # Relationship with Coach
#     coach = relationship("Coach", back_populates="metrics")


from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func, Sequence, ForeignKey, Numeric, Boolean, \
    CheckConstraint
from sqlalchemy.orm import relationship

from app.domain.models.base import Base


class Coach(Base):
    __tablename__ = "coach"

    id = Column(Integer, Sequence("coach_id_seq"), primary_key=True)
    password = Column(String(255), nullable=False)
    user_name = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    gender = Column(String(10))
    status = Column(Boolean, default=False)
    date_of_birth = Column(String(15))
    image = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())
    is_verified = Column(Boolean, default=False)

    metrics = relationship("CoachMetrics", back_populates="coach", uselist=False)


class CoachMetrics(Base):
    __tablename__ = 'coach_metrics'

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey('coach.id', ondelete='CASCADE'), unique=True)
    height = Column(Numeric(5, 2))
    weight = Column(Numeric(5, 2))
    specialization = Column(String(255))
    biography = Column(Text)

    rating = Column(Integer, default=0)
    coaching_id = Column(String(100), nullable=False)
    coaching_card_image = Column(Text)

    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint('rating BETWEEN 0 AND 5', name='check_coach_rating_range'),
    )

    # Relationship with Coach
    coach = relationship("Coach", back_populates="metrics")
