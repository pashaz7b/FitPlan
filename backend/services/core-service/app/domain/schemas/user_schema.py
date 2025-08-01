from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, constr


class GetUserInfoSchema(BaseModel):
    password: Optional[str] = None
    user_name: str
    name: str
    email: str
    phone_number: constr(max_length=20)
    gender: Optional[constr(max_length=10)]
    date_of_birth: Optional[str]
    height: Optional[float]
    weight: Optional[float]
    # waist: Optional[float]
    # injuries: Optional[str]
    # image: Optional[str]


class SetUserInfoSchema(BaseModel):
    password: Optional[str]
    user_name: Optional[str]
    name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    gender: Optional[str]
    date_of_birth: Optional[str]
    height: Optional[float]
    weight: Optional[float]


class SetUserInfoResponseSchema(BaseModel):
    message: str


class GetUserTransactionsSchema(BaseModel):
    id: int
    amount: float
    reason: str
    status: str
    date: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class GetUserCoachSchema(BaseModel):
    user_name: str
    name: str
    email: str
    phone_number: str
    gender: str
    date_of_birth: str
    height: float
    weight: float
    specialization: str
    biography: str
    status: bool


class UserRequestExerciseSchema(BaseModel):
    weight: float
    waist: float
    type: str


class UserRequestExerciseResponseSchema(BaseModel):
    weight: float
    waist: float
    type: str
    price: int
    msg: str


class GetUserExerciseSchema(BaseModel):
    id: int
    day: str
    name: str
    set: str
    expire_time: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ExerciseSchema(BaseModel):
    id: int
    day: str
    name: str
    set: str
    expire_time: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class GroupedExerciseSchema(BaseModel):
    created_at: str
    coach_name: str
    coach_email: str
    exercises: List[ExerciseSchema]


class SetUserTransactionsSchema(BaseModel):
    amount: float
    reason: str
    status: str
    date: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ********************************************************************************
class UserRequestMealSchema(BaseModel):
    weight: float
    waist: float
    type: str


class UserRequestMealResponseSchema(BaseModel):
    weight: float
    waist: float
    type: str
    price: int
    msg: str


class GetUserMealSchema(BaseModel):
    created_date: str
    coach_name: str
    coach_email: str
    id: int
    breakfast: str
    lunch: str
    dinner: str
    supplement: str
    expire_time: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ********************************************************************************
class GetUserAllCoachSchema(BaseModel):
    work_out_plan_id: int
    work_out_plan_name: str
    work_out_plan_description: str
    work_out_plan_duration_month: int
    coach_user_name: str
    coach_name: str
    coach_email: str
    coach_phone_number: str
    coach_gender: str
    coach_date_of_birth: str
    coach_height: float
    coach_weight: float
    coach_specialization: str
    coach_biography: str
    coach_status: bool
    coach_rating: int


class UserTakeWorkoutCoachSchema(BaseModel):
    work_out_plan_id: int


class UserTakeWorkoutCoachResponseSchema(BaseModel):
    work_out_plan_id: int
    msg: str


class ChangeUserCoach(BaseModel):
    new_workout_plan_id: int


class ChangeUserCoachResponse(BaseModel):
    message: str


# ********************************************************************************

class UserGetAllVerifiedGymSchema(BaseModel):
    gym_id: int
    gym_name: str
    gym_location: str


class UserGetVerifiedGymDetailSchema(BaseModel):
    gym_id: int
    gym_owner_id: int
    gym_name: str
    gym_location: str
    gym_sport_facilities: str
    gym_welfare_facilities: str
    gym_rating: int


class UserGetVerifiedGymCoachesSchema(BaseModel):
    work_out_plan_id: int
    work_out_plan_name: str
    work_out_plan_description: str
    work_out_plan_duration_month: int
    coach_id: int
    coach_user_name: str
    coach_name: str
    coach_email: str
    coach_phone_number: str
    coach_gender: str
    coach_date_of_birth: str
    coach_height: float
    coach_weight: float
    coach_specialization: str
    coach_biography: str
    coach_status: bool
    coach_rating: int


class UserGetVerifiedGymPlanPriceSchema(BaseModel):
    session_counts: int
    duration_days: int
    is_vip: bool
    price: int


class UserGetVerifiedGymCommentsSchema(BaseModel):
    users_name: str
    comment: str
    rating: int
    date: str


class CreateUserGymRegistrationSchema(BaseModel):
    # user_id: int
    gym_id: int
    registered_sessions: int
    registered_days: int
    is_vip: bool
    price: int
    # remaining_sessions: int
    # remaining_days: int
    # is_expired: int
    # date: str


class CreateUserGymRegistrationResponseSchema(BaseModel):
    registration_id: int
    message: str


class UserGetGymRegistrationsSchema(BaseModel):
    gym_id: int
    gym_name: str
    registered_sessions: int
    registered_days: int
    is_vip: bool
    remaining_sessions: int
    remaining_days: int
    is_expired: bool
    date: str


class CreateUserGymCommentSchema(BaseModel):
    gym_id: int
    comment: str
    rating: int


class CreateUserGymCommentResponseSchema(BaseModel):
    registered_comment_id: int
    message: str


# *******************************************************************

class UserGetVerifiedCoachCommentsSchema(BaseModel):
    users_name: str
    comment: str
    rating: int
    date: str


class CreateUserCoachCommentSchema(BaseModel):
    coach_id: int
    comment: str
    rating: int


class CreateUserCoachCommentResponseSchema(BaseModel):
    registered_comment_id: int
    message: str


class UserGetCoachPlanPriceSchema(BaseModel):
    exercise_price: int
    meal_price: int
