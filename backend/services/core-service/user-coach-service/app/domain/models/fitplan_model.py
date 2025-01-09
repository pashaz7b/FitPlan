from sqlalchemy import (Column, Integer, String, Text, TIMESTAMP, func, Sequence, ForeignKey, Numeric, Boolean,
                        DECIMAL)
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
    user_transactions = relationship("UserTransactionLog", back_populates="user")

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
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    # Relationship with Coach
    coach = relationship("Coach", back_populates="metrics")



class UserDuplicates(Base):
    __tablename__ = 'user_duplicates'
    id = Column(Integer, Sequence('user_duplicates_id_seq'), primary_key=True)
    user_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)



class TransactionLog(Base):
    __tablename__ = 'transaction_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    reason = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    date = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user_transaction = relationship("UserTransactionLog", back_populates="transaction")

class UserTransactionLog(Base):
    __tablename__ = 'user_transaction_log'

    transaction_id = Column(Integer, ForeignKey('transaction_log.id', ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    transaction = relationship("TransactionLog", back_populates="user_transaction")
    user = relationship("User", back_populates="user_transactions")