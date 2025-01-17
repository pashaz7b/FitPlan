from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func, Sequence, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, Sequence("admin_id_seq"), primary_key=True)
    password = Column(String(255), nullable=False)
    user_name = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    gender = Column(String(10))
    date_of_birth = Column(String(15))
    image = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())
    is_verified = Column(Boolean, default=False)