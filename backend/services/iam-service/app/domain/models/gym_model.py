from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, CheckConstraint
from sqlalchemy.sql import func
from app.domain.models.base import Base


class Gym(Base):
    __tablename__ = "gym"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("coach.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False)
    license_number = Column(String(100), nullable=False)
    license_image = Column(Text, nullable=True)
    location = Column(Text, nullable=True)
    image = Column(Text, nullable=True)
    sport_facilities = Column(Text, nullable=True)
    welfare_facilities = Column(Text, nullable=True)

    rating = Column(Integer, default=0)
    verification_status = Column(String(50), default="pending")

    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint('rating BETWEEN 0 AND 5', name='check_rating_range'),
    )
