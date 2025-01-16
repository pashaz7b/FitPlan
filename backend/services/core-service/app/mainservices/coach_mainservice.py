from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status

from app.domain.schemas.coach_schema import (GetCoachUserSchema, SetCoachUserMealSchema, GetCoachUserMealRequestSchema,
                                             GetCoachUserExerciseRequestSchema, SetCoachUserExerciseSchema,
                                             GetCoachInfoSchema, SetCoachWorkOutPlanSchema
                                             )

from app.subservices.coach_subservice import CoachSubService
from app.subservices.user_duplicates_subservice import UserDuplicatesSubService
from app.subservices.baseconfig import BaseService
from app.subservices.auth.hash_subservice import HashService


class CoachMainService(BaseService):
    def __init__(self,
                 coach_subservice: Annotated[CoachSubService, Depends()],
                 user_duplicates_subservice: Annotated[UserDuplicatesSubService, Depends()],
                 hash_subservice: Annotated[HashService, Depends()]
                 ) -> None:
        super().__init__()
        self.coach_subservice = coach_subservice
        self.user_duplicates_subservice = user_duplicates_subservice
        self.hash_subservice = hash_subservice

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

    async def get_coach_info(self, coach_id: int) -> GetCoachInfoSchema:
        coach = await self.coach_subservice.get_coach(coach_id)
        coach_metrics = await self.coach_subservice.get_coach_metrics(coach_id)
        empty_password = ""
        return GetCoachInfoSchema(
            password=empty_password,
            user_name=coach.user_name,
            name=coach.name,
            email=coach.email,
            phone_number=coach.phone_number,
            gender=coach.gender,
            status=coach.status,
            date_of_birth=coach.date_of_birth,
            height=coach_metrics.height,
            weight=coach_metrics.weight,
            specialization=coach_metrics.specialization,
            biography=coach_metrics.biography
        )

    async def change_coach_info(self, coach_id: int, coach: GetCoachInfoSchema):
        current_coach = await self.coach_subservice.get_coach(coach_id)
        current_coach_metrics = await self.coach_subservice.get_coach_metrics(coach_id)

        current_data = {
            "password": current_coach.password,
            "user_name": current_coach.user_name,
            "name": current_coach.name,
            "email": current_coach.email,
            "phone_number": current_coach.phone_number,
            "gender": current_coach.gender,
            "status": current_coach.status,
            "date_of_birth": current_coach.date_of_birth,
            "height": current_coach_metrics.height,
            "weight": current_coach_metrics.weight,
            "specialization": current_coach_metrics.specialization,
            "biography": current_coach_metrics.biography
        }

        if coach.password.strip():
            coach.password = self.hash_subservice.hash_password(coach.password) if coach.password else None

        changes = {key: value for key, value in coach if current_data.get(key) != value}

        if not coach.password.strip():
            changes.pop("password")

        if "email" in changes:
            await self.check_email_existence(coach.email)

        if "phone_number" in changes:
            await self.check_phone_number_existence(coach.phone_number)

        if "user_name" in changes:
            await self.check_user_name_existence(coach.user_name)

        if changes:
            await self.coach_subservice.change_coach_info(coach_id, changes)

        return {"message": "Coach information updated successfully" if changes else "No changes detected"}

    async def get_coach_user(self, coach_id: int):
        logger.info("[+] Fetching Users of The Coach With ID ---> {coach_id}")

        coach_users = await self.coach_subservice.get_coach_user(coach_id)

        if not coach_users:
            logger.error(f"[-] No User Found For This Coach With ID ---> {coach_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No User Found For This Coach"
            )

        coach_users_schema = [
            GetCoachUserSchema(
                id=coach_user.id,
                user_name=coach_user.user_name,
                name=coach_user.name,
                email=coach_user.email,
                phone_number=coach_user.phone_number,
                gender=coach_user.gender,
                date_of_birth=coach_user.date_of_birth,
                height=coach_user.metrics.height,
                weight=coach_user.metrics.weight
            )
            for coach_user in coach_users
        ]

        return coach_users_schema

    async def get_coach_user_meal_request(self, coach_id: int):
        logger.info("[+] Fetching Users Meal Request of The Coach With ID ---> {coach_id}")

        coach_user_meal_request = await self.coach_subservice.get_coach_user_meal_request(coach_id)

        if not coach_user_meal_request:
            logger.error(f"[-] No User Meal Request Found For This Coach With ID ---> {coach_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No User Meal Request Found For This Coach"
            )

        result = []
        for user in coach_user_meal_request:
            for request_meal in user.user_request_meals:
                flag = await self.coach_subservice.get_is_answered_requested_meal(request_meal.user_meal.id)
                if not flag:
                    for take in user.takes:
                        result.append(GetCoachUserMealRequestSchema(
                            work_out_plan_id=take.workout_plan.id,
                            work_out_plan_name=take.workout_plan.name,
                            user_meal_id=request_meal.user_meal.id,
                            user_meal_weight=request_meal.user_meal.weight,
                            user_meal_waist=request_meal.user_meal.waist,
                            user_meal_type=request_meal.user_meal.type,
                            user_id=user.id,
                            user_name=user.name,
                            name=user.name,
                            email=user.email,
                            phone_number=user.phone_number,
                            gender=user.gender,
                            date_of_birth=user.date_of_birth,
                        ))

        return result

    async def create_coach_user_meal(self, coach_id: int, meal: SetCoachUserMealSchema):
        logger.info(f"[+] Creating Coach User Meal With Coach ID ---> {coach_id}")

        return await self.coach_subservice.create_coach_user_meal(coach_id, meal)

    async def get_coach_user_exercise_request(self, coach_id: int):
        logger.info(f"[+] Fetching User Exercise Request For Coach With Id ---> {coach_id}")

        coach_user_exercise_request = await self.coach_subservice.get_coach_user_exercise_request(coach_id)

        if not coach_user_exercise_request:
            logger.error(f"[-] No User Exercise Request Found For This Coach With ID ---> {coach_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No User Exercise Request Found For This Coach"
            )

        result = []

        for user in coach_user_exercise_request:
            for request_exercise in user.user_requests:
                flag = await self.coach_subservice.get_is_answered_requested_exercise(request_exercise.exercise.id)
                if not flag:
                    for take in user.takes:
                        result.append(GetCoachUserExerciseRequestSchema(
                            work_out_plan_id=take.workout_plan.id,
                            work_out_plan_name=take.workout_plan.name,
                            user_exercise_id=request_exercise.exercise.id,
                            user_exercise_weight=request_exercise.exercise.weight,
                            user_exercise_waist=request_exercise.exercise.waist,
                            user_exercise_type=request_exercise.exercise.type,
                            user_id=user.id,
                            user_name=user.name,
                            name=user.name,
                            email=user.email,
                            phone_number=user.phone_number,
                            gender=user.gender,
                            date_of_birth=user.date_of_birth,
                        ))

        return result

    async def create_coach_user_exercise(self, coach_id: int, user_exercise_id: int, work_out_plan_id: int,
                                         exercises: list[SetCoachUserExerciseSchema]):
        logger.info(f"[+] Creating Coach User Exercise With Coach ID ---> {coach_id}")

        return await self.coach_subservice.create_coach_user_exercise(coach_id, user_exercise_id, work_out_plan_id,
                                                                      exercises)

    async def create_workout_plan(self, coach_id: int, workout_plan: SetCoachWorkOutPlanSchema):
        logger.info(f"[+] Creating Workout Plan With Coach ID ---> {coach_id}")

        return await self.coach_subservice.create_workout_plan(coach_id, workout_plan)
