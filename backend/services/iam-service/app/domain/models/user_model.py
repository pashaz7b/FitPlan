from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Numeric,
    Text,
    ForeignKey,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(255), nullable=False)
    user_name = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True)
    gender = Column(String(10))
    date_of_birth = Column(String(15))
    image = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())
    is_verified = Column(Boolean, default=False)

    metrics = relationship("UserMetrics", back_populates="user", uselist=False)


class UserMetrics(Base):
    __tablename__ = 'user_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    height = Column(Numeric(5, 2))
    weight = Column(Numeric(5, 2))
    waist = Column(Numeric(5, 2))
    injuries = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="metrics")