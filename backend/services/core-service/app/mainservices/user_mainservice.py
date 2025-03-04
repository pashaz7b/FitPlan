from pyexpat.errors import messages
from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status
from collections import defaultdict
from typing import Dict

from app.domain.schemas.user_schema import (GetUserInfoSchema,
                                            SetUserInfoSchema,
                                            GetUserTransactionsSchema,
                                            GetUserCoachSchema,
                                            UserRequestExerciseSchema,
                                            GetUserExerciseSchema, UserRequestMealSchema, GetUserMealSchema,
                                            GetUserAllCoachSchema, UserTakeWorkoutCoachSchema,
                                            UserTakeWorkoutCoachResponseSchema, GroupedExerciseSchema, ExerciseSchema,
                                            ChangeUserCoachResponse)

from app.subservices.user_subservice import UserSubService
from app.subservices.user_duplicates_subservice import UserDuplicatesSubService
from app.subservices.baseconfig import BaseService
from app.subservices.auth.hash_subservice import HashService


class UserMainService(BaseService):
    def __init__(self,
                 user_subservice: Annotated[UserSubService, Depends()],
                 user_duplicates_subservice: Annotated[UserDuplicatesSubService, Depends()],
                 hash_subservice: Annotated[HashService, Depends()]
                 ) -> None:
        super().__init__()
        self.user_subservice = user_subservice
        self.user_duplicates_subservice = user_duplicates_subservice
        self.hash_subservice = hash_subservice

    async def check_existence(self, user: SetUserInfoSchema):
        existing_user_email = await self.user_duplicates_subservice.get_user_by_email(user.email)
        existing_user_phone_number = await self.user_duplicates_subservice.get_user_by_phone_number(user.phone_number)
        existing_user_name = await self.user_duplicates_subservice.get_user_by_user_name(user.user_name)
        # coach and admin user_duplicate

        if existing_user_email:
            logger.error(f"[-] User Email ---> {user.email} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User With This Email Already Exists"
            )

        if existing_user_phone_number:
            logger.error(f"[-] User Phone Number ---> {user.phone_number} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User With This Phone Number Already  Exists"
            )

        if existing_user_name:
            logger.error(f"[-] User Name ---> {user.user_name} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User With This User Name Already Exists"
            )

    async def check_email_existence(self, email: str):
        existing_user_email = await self.user_duplicates_subservice.get_user_by_email(email)
        if existing_user_email:
            logger.error(f"[-] User Email ---> {email} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User With This Email Already Exists"
            )

    async def check_phone_number_existence(self, phone_number: str):
        existing_user_phone_number = await self.user_duplicates_subservice.get_user_by_phone_number(phone_number)
        if existing_user_phone_number:
            logger.error(f"[-] User Phone Number ---> {phone_number} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User With This Phone Number Already Exists"
            )

    async def check_user_name_existence(self, user_name: str):
        existing_user_name = await self.user_duplicates_subservice.get_user_by_user_name(user_name)
        if existing_user_name:
            logger.error(f"[-] User Name ---> {user_name} Already Exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User With This User Name Already Exists"
            )

    # async def register_user(self, user: UserRegisterSchema) -> UserRegisterResponseSchema:
    #     await self.check_existence(user)
    #
    #     # else:
    #     new_user = await self.user_subservice.create_user(user)
    #     otp = self.otp_subservice.send_otp(new_user.email)
    #
    #     logger.info(f"[+] User With Email --> {user.email} Created Successfully")
    #     response = UserRegisterResponseSchema(
    #         id=new_user.id,
    #         user_name=new_user.user_name,
    #         name=new_user.name,
    #         email=new_user.email,
    #         is_verified=new_user.is_verified,
    #         created_at=new_user.created_at,
    #         updated_at=new_user.updated_at,
    #         message="User Created Successfully, OTP Sent To The Email"
    #     )
    #     return response

    async def get_user_info(self, user_id: int) -> GetUserInfoSchema:
        user = await self.user_subservice.get_user(user_id)
        user_metrics = await self.user_subservice.get_user_metrics(user_id)
        empty_password = ""
        return GetUserInfoSchema(
            id=user.id,
            password=empty_password,
            user_name=user.user_name,
            name=user.name,
            email=user.email,
            phone_number=user.phone_number,
            gender=user.gender,
            date_of_birth=user.date_of_birth,
            height=user_metrics.height,
            weight=user_metrics.weight)

    async def change_user_info(self, user_id: int, user: SetUserInfoSchema):

        current_user = await self.user_subservice.get_user(user_id)
        current_user_metrics = await self.user_subservice.get_user_metrics(user_id)

        current_data = {
            "password": current_user.password,
            "user_name": current_user.user_name,
            "name": current_user.name,
            "email": current_user.email,
            "phone_number": current_user.phone_number,
            "gender": current_user.gender,
            "date_of_birth": current_user.date_of_birth,
            "height": current_user_metrics.height,
            "weight": current_user_metrics.weight,
        }

        if user.password.strip():
            user.password = self.hash_subservice.hash_password(user.password) if user.password else None

        changes = {key: value for key, value in user if current_data.get(key) != value}

        if not user.password.strip():
            changes.pop("password")

        logger.info(f"change {changes}")
        if "email" in changes:
            await self.check_email_existence(user.email)

        if "phone_number" in changes:
            await self.check_phone_number_existence(user.phone_number)

        if "user_name" in changes:
            await self.check_user_name_existence(user.user_name)

        if changes:
            await self.user_subservice.change_user_info(user_id, changes)

        return {"message": "User information updated successfully" if changes else "No changes detected"}

    async def get_user_transaction_log(self, user_id: int):
        logger.info(f"[+] Fetching Transaction Logs For User With Id ---> {user_id}")
        transaction_logs = await self.user_subservice.get_user_transaction_log(user_id)

        if not transaction_logs:
            logger.info(f"[-] No transactions found for user with id ---> {user_id}")
            raise HTTPException(status_code=404, detail="No transactions found for this user")

        transaction_schemas = [
            GetUserTransactionsSchema(
                id=transaction_log.id,
                amount=transaction_log.amount,
                reason=transaction_log.reason,
                status=transaction_log.status,
                date=transaction_log.date,
                created_at=transaction_log.created_at,
                updated_at=transaction_log.updated_at
            )
            for transaction_log in transaction_logs
        ]

        return transaction_schemas

    async def get_user_coach(self, user_id: int) -> GetUserCoachSchema:
        logger.info(f"[...] Fetching Coach For User With Id ---> {user_id}")
        coach = await self.user_subservice.get_user_coach(user_id)

        if not coach:
            logger.info(f"[-] No coach found for user with id ---> {user_id}")
            raise HTTPException(status_code=404, detail="No coach found for this user")

        return GetUserCoachSchema(
            user_name=coach.user_name,
            name=coach.name,
            email=coach.email,
            phone_number=coach.phone_number,
            gender=coach.gender,
            date_of_birth=coach.date_of_birth,
            height=coach.metrics.height,
            weight=coach.metrics.weight,
            specialization=coach.metrics.specialization,
            biography=coach.metrics.biography,
            status=coach.status)

    async def create_user_exercise(self, user_id, user_struct: UserRequestExerciseSchema):
        logger.info(f"[+] Creating Request Exercise For User With Id ---> {user_id}")

        if not await self.get_user_coach(user_id):
            logger.info(f"[-] No coach found for user with id ---> {user_id}")
            raise HTTPException(status_code=404, detail="No coach found for this user")

        return await self.user_subservice.create_user_exercise(user_id, user_struct)

    async def get_user_exercise(self, user_id):
        logger.info(f"[+] Fetching Exercise For User With Id ---> {user_id}")

        fetched_exercises = await self.user_subservice.get_user_exercise(user_id)

        if not fetched_exercises:
            logger.info(f"[-] No exercise found for user with id ---> {user_id}")
            raise HTTPException(status_code=404, detail="No exercise found for this user")

        grouped_exercises = defaultdict(list)
        for exercise in fetched_exercises:
            created_at_date = exercise.created_at.replace(second=0, microsecond=0)
            grouped_exercises[created_at_date].append(exercise)

        response = []
        for created_at, exercises in grouped_exercises.items():
            response.append(GroupedExerciseSchema(
                created_at=created_at.isoformat(),
                coach_name=exercises[0].workout_plans[0].workout_plan.present[0].coach.name,
                coach_email=exercises[0].workout_plans[0].workout_plan.present[0].coach.email,
                exercises=[
                    ExerciseSchema(
                        id=exercise.id,
                        day=exercise.day,
                        name=exercise.name,
                        set=exercise.set,
                        expire_time=exercise.expire_time,
                        created_at=exercise.created_at,
                        updated_at=exercise.updated_at
                    )
                    for exercise in exercises
                ]
            ))

        return response

    async def create_user_meal(self, user_id, user_struct: UserRequestMealSchema):
        logger.info(f"[+] Creating Request Meal For User With Id ---> {user_id}")

        if not await self.get_user_coach(user_id):
            logger.info(f"[-] No coach found for user with id ---> {user_id}")
            raise HTTPException(status_code=404, detail="No coach found for this user")

        return await self.user_subservice.create_user_meal(user_id, user_struct)

    async def get_user_meal(self, user_id):
        logger.info(f"[+] Fetching Meal For User With Id ---> {user_id}")

        fetched_meals = await self.user_subservice.get_user_meal(user_id)

        if not fetched_meals:
            logger.info(f"[-] No meal found for user with id ---> {user_id}")
            raise HTTPException(status_code=404, detail="No meal found for this user")

        grouped_meals = defaultdict(list)
        for meal in fetched_meals:
            created_at_date = meal.created_at.replace(second=0, microsecond=0)
            grouped_meals[created_at_date].append(meal)

        response = []
        for created_at, meals in grouped_meals.items():
            meal = meals[0]
            response.append(GetUserMealSchema(
                created_date=created_at.isoformat(),
                coach_name=meal.workout_plan_meal_supplements[0].workout_plan.present[0].coach.name,
                coach_email=meal.workout_plan_meal_supplements[0].workout_plan.present[0].coach.email,
                id=meal.id,
                breakfast=meal.breakfast,
                lunch=meal.lunch,
                dinner=meal.dinner,
                supplement=meal.supplement,
                expire_time=meal.expire_time,
                created_at=meal.created_at,
                updated_at=meal.updated_at
            ))

        return response

    async def get_user_all_coach(self, user_id: int):
        logger.info(f"[...] Fetching All Coaches For User With Id ---> {user_id}")
        coaches = await self.user_subservice.get_user_all_coach(user_id)

        if not coaches:
            logger.info(f"[-] There is no Active Coach")
            raise HTTPException(status_code=404, detail="There is no Active Coach")

        result = []
        for coach in coaches:
            for present in coach.present:
                workout_plan = present.workout_plan
                result.append(GetUserAllCoachSchema(
                    work_out_plan_id=workout_plan.id,
                    work_out_plan_name=workout_plan.name,
                    work_out_plan_description=workout_plan.description,
                    work_out_plan_duration_month=workout_plan.duration_month,
                    coach_user_name=coach.user_name,
                    coach_name=coach.name,
                    coach_email=coach.email,
                    coach_phone_number=coach.phone_number,
                    coach_gender=coach.gender,
                    coach_date_of_birth=coach.date_of_birth,
                    coach_height=coach.metrics.height,
                    coach_weight=coach.metrics.weight,
                    coach_specialization=coach.metrics.specialization,
                    coach_biography=coach.metrics.biography,
                    coach_status=coach.status
                ))

        return result

        # coach_schemas = [
        #     GetUserAllCoachSchema(
        #         id=coach.id,
        #         user_name=coach.user_name,
        #         name=coach.name,
        #         email=coach.email,
        #         phone_number=coach.phone_number,
        #         gender=coach.gender,
        #         date_of_birth=coach.date_of_birth,
        #         height=coach.metrics.height,
        #         weight=coach.metrics.weight,
        #         specialization=coach.metrics.specialization,
        #         biography=coach.metrics.biography,
        #         status=coach.status
        #     )
        #     for coach in coaches
        # ]
        #
        # return coach_schemas

    async def create_user_take_workout_coach(self, user_id: int, take_strucr: UserTakeWorkoutCoachSchema):
        logger.info(f"[+] User With Id ---> {user_id} Take Workout With Id ---> {take_strucr.work_out_plan_id}")

        existed_workout_coach = await self.user_subservice.check_if_user_take_workout_coach_exists(user_id)

        if existed_workout_coach:
            logger.info(f"[-] User With Id ---> {user_id} Already Take Workout")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Already Take Workout Coach")

        result = await self.user_subservice.create_user_take_workout_coach(user_id, take_strucr)

        return UserTakeWorkoutCoachResponseSchema(
            work_out_plan_id=take_strucr.work_out_plan_id,
            msg="Workout Plan Taken Successfully"
        )

    async def update_user_coach(self, user_id: int, updated_user: Dict):
        await self.user_subservice.update_user_coach(user_id, updated_user)

        return ChangeUserCoachResponse(
            message="Coach Changed Successfully"
        )
