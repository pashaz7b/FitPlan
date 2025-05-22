from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func, Boolean, Sequence
from app.domain.models.base import Base


class UserDuplicates(Base):
    __tablename__ = 'user_duplicates'
    id = Column(Integer, Sequence('user_duplicates_id_seq'), primary_key=True)
    user_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)