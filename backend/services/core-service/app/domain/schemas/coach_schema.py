from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr


class GetCoachInfoSchema(BaseModel):
    password: Optional[str] = None
    user_name: str
    name: str
    email: str
    phone_number: constr(max_length=20)
    gender: Optional[constr(max_length=10)]
    status: bool
    date_of_birth: Optional[str]
    height: Optional[float]
    weight: Optional[float]
    specialization: Optional[str]
    biography: Optional[str]


class SetCoachInfoSchema(BaseModel):
    password: Optional[str]
    user_name: Optional[str]
    name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    gender: Optional[str]
    status: Optional[bool]
    date_of_birth: Optional[str]
    height: Optional[float]
    weight: Optional[float]
    specialization: Optional[str]
    biography: Optional[str]


class GetCoachUserSchema(BaseModel):
    id: int
    user_name: str
    name: str
    email: str
    phone_number: str
    gender: str
    date_of_birth: str
    height: float
    weight: float


class GetCoachUserMealRequestSchema(BaseModel):
    work_out_plan_id: int
    work_out_plan_name: str
    user_meal_id: int
    user_meal_weight: float
    user_meal_waist: float
    user_meal_type: str
    user_id: int
    user_name: str
    name: str
    email: str
    phone_number: str
    gender: str
    date_of_birth: str


class SetCoachUserMealSchema(BaseModel):
    work_out_plan_id: int
    user_meal_id: int
    breakfast: str
    lunch: str
    dinner: str
    supplement: Optional[str] = None
    expire_time: Optional[int] = None


class SetCoachUserMealResponseSchema(BaseModel):
    meal_id: int
    message: str


class GetCoachUserExerciseRequestSchema(BaseModel):
    work_out_plan_id: int
    work_out_plan_name: str
    user_exercise_id: int
    user_exercise_weight: float
    user_exercise_waist: float
    user_exercise_type: str
    user_id: int
    user_name: str
    name: str
    email: str
    phone_number: str
    gender: str
    date_of_birth: str


class SetCoachUserExerciseSchema(BaseModel):
    day: str
    name: str
    set: str
    expire_time: Optional[int] = None


class SetCoachUserExerciseResponseSchema(BaseModel):
    message: str


class SetCoachWorkOutPlanSchema(BaseModel):
    workout_plan_name: str
    workout_plan_description: str
    workout_plan_duration_month: Optional[int] = None


class SetCoachWorkOutPlanResponseSchema(BaseModel):
    workout_plan_id: int
    message: str


# ********************************************************************

class CoachGetCoachPlanPriceSchema(BaseModel):
    exercise_price: int
    meal_price: int


class CoachCreateCoachPlanPriceSchema(BaseModel):
    exercise_price: int
    meal_price: int


class CoachCreateCoachPlanPriceResponseSchema(BaseModel):
    created_coach_plan_price_id: int
    message: str


class CoachChangeCoachPlanPriceSchema(BaseModel):
    exercise_price: int
    meal_price: int


class CoachChangeCoachPlanPriceResponseSchema(BaseModel):
    message: str


class CoachGetHisGymInfoSchema(BaseModel):
    gym_id: int
    gym_name: str


class CoachGetGymPlanPriceSchema(BaseModel):
    plan_price_id: int
    session_counts: int
    duration_days: int
    is_vip: bool
    price: int


class CoachCreateGymPlanPriceSchema(BaseModel):
    session_counts: int
    duration_days: int
    is_vip: bool
    price: int


class CoachCreateGymPlanPriceResponseSchema(BaseModel):
    plan_price_id: int
    message: str


class CoachDeleteGymPlanPriceSchema(BaseModel):
    plan_price_id: int


class CoachDeleteGymPlanPriceResponseSchema(BaseModel):
    message: str


class CoachChangeGymPlanPriceSchema(BaseModel):
    plan_price_id: int
    session_counts: int
    duration_days: int
    is_vip: bool
    price: int


class CoachChangeGymPlanPriceResponseSchema(BaseModel):
    message: str
