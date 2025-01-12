from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr


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
