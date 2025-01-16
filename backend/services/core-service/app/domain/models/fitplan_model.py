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
    # workout_plans = relationship('WorkoutPlan', secondary='take', back_populates='user')
    takes = relationship('Take', back_populates='user')
    user_requests = relationship("UserRequestExercise", back_populates="user")
    user_request_meals = relationship("UserRequestMeal", back_populates="user")


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
    present = relationship('Present', back_populates='coach')


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


class WorkoutPlan(Base):
    __tablename__ = 'workout_plan'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    duration_month = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    # users = relationship('User', secondary='take', back_populates='workout_plans')
    # coach = relationship('Coach', secondary='present', back_populates='workout_plans')
    takes = relationship('Take', back_populates='workout_plan')
    present = relationship('Present', back_populates='workout_plan')
    exercises = relationship("WorkoutPlanExercise", back_populates="workout_plan")
    workout_plan_meal_supplements = relationship("WorkoutPlanMealSupplement", back_populates="workout_plan")


class Take(Base):
    __tablename__ = 'take'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    workout_plan_id = Column(Integer, ForeignKey('workout_plan.id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    user = relationship('User', back_populates='takes')
    workout_plan = relationship('WorkoutPlan', back_populates='takes')


class Present(Base):
    __tablename__ = 'present'

    coach_id = Column(Integer, ForeignKey('coach.id', ondelete='CASCADE'), primary_key=True)
    workout_plan_id = Column(Integer, ForeignKey('workout_plan.id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    coach = relationship('Coach', back_populates='present')
    workout_plan = relationship('WorkoutPlan', back_populates='present')


class UserExercise(Base):
    __tablename__ = 'user_exercise'

    id = Column(Integer, primary_key=True, autoincrement=True)
    weight = Column(DECIMAL(5, 2), nullable=False)
    waist = Column(DECIMAL(5, 2), nullable=False)
    type = Column(String(10), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    image = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(),
                        nullable=False)

    user_requests = relationship("UserRequestExercise", back_populates="exercise")
    exercise_links = relationship("UserExerciseExercise", back_populates="user_exercise")


class UserRequestExercise(Base):
    __tablename__ = 'user_request_exercise'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_exercise_id = Column(Integer, ForeignKey('user_exercise.id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    user = relationship("User", back_populates="user_requests")
    exercise = relationship("UserExercise", back_populates="user_requests")


class Exercise(Base):
    __tablename__ = 'exercise'

    id = Column(Integer, primary_key=True, autoincrement=True)
    day = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    set = Column(String(100), nullable=False)
    expire_time = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(),
                        nullable=False)

    # Relationship to workout_plan_exercise
    workout_plans = relationship("WorkoutPlanExercise", back_populates="exercise")
    user_exercise_links = relationship("UserExerciseExercise", back_populates="exercise")


class WorkoutPlanExercise(Base):
    __tablename__ = 'workout_plan_exercise'

    exercise_id = Column(Integer, ForeignKey('exercise.id', ondelete='CASCADE'), primary_key=True)
    workout_plan_id = Column(Integer, ForeignKey('workout_plan.id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    exercise = relationship("Exercise", back_populates="workout_plans")
    workout_plan = relationship("WorkoutPlan", back_populates="exercises")


class UserExerciseExercise(Base):
    __tablename__ = 'user_exercise_exercise'

    exercise_id = Column(Integer, ForeignKey('exercise.id', ondelete='CASCADE'), primary_key=True)
    user_exercise_id = Column(Integer, ForeignKey('user_exercise.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    exercise = relationship("Exercise", back_populates="user_exercise_links")
    user_exercise = relationship("UserExercise", back_populates="exercise_links")


class UserMeal(Base):
    __tablename__ = "user_meal"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    weight = Column(DECIMAL(5, 2), nullable=False)
    waist = Column(DECIMAL(5, 2), nullable=False)
    type = Column(String(10), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    image = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user_requests = relationship("UserRequestMeal", back_populates="user_meal")
    user_meal_meal_supplement = relationship("UserMealMealSupplement", back_populates="user_meal")


class UserRequestMeal(Base):
    __tablename__ = "user_request_meal"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user_meal_id = Column(Integer, ForeignKey("user_meal.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="user_request_meals")
    user_meal = relationship("UserMeal", back_populates="user_requests")


class MealSupplement(Base):
    __tablename__ = "meal_supplement"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    breakfast = Column(Text, nullable=True)
    lunch = Column(Text, nullable=True)
    dinner = Column(Text, nullable=True)
    supplement = Column(Text, nullable=True)
    expire_time = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    workout_plan_meal_supplements = relationship("WorkoutPlanMealSupplement", back_populates="meal_supplement")
    user_meal_meal_supplements = relationship("UserMealMealSupplement", back_populates="meal_supplement")


class WorkoutPlanMealSupplement(Base):
    __tablename__ = "workout_plan_meal_supplement"

    meal_supplement_id = Column(Integer, ForeignKey("meal_supplement.id", ondelete="CASCADE"), primary_key=True)
    workout_plan_id = Column(Integer, ForeignKey("workout_plan.id", ondelete="CASCADE"), primary_key=True)

    # Relationships
    meal_supplement = relationship("MealSupplement", back_populates="workout_plan_meal_supplements")
    workout_plan = relationship("WorkoutPlan", back_populates="workout_plan_meal_supplements")


class UserMealMealSupplement(Base):
    __tablename__ = "user_meal_meal_supplement"

    meal_supplement_id = Column(Integer, ForeignKey("meal_supplement.id", ondelete="CASCADE"), primary_key=True)
    user_meal_id = Column(Integer, ForeignKey("user_meal.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Relationships
    meal_supplement = relationship("MealSupplement", back_populates="user_meal_meal_supplements")
    user_meal = relationship("UserMeal", back_populates="user_meal_meal_supplement")


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
