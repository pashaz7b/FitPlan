from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status

from app.domain.schemas.coach_schema import (GetCoachUserSchema, SetCoachUserMealSchema,
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
                        result.append({
                            "work_out_plan_id": take.workout_plan.id,
                            "work_out_plan_name": take.workout_plan.name,
                            "user_meal_id": request_meal.user_meal.id,
                            "user_meal_weight": request_meal.user_meal.weight,
                            "user_meal_waist": request_meal.user_meal.waist,
                            "user_meal_type": request_meal.user_meal.type,
                            "user_id": user.id,
                            "user_name": user.name,
                            "name": user.name,
                            "email": user.email,
                            "phone_number": user.phone_number,
                            "gender": user.gender,
                            "date_of_birth": user.date_of_birth,
                        })

        return result

    async def create_coach_user_meal(self, coach_id: int, meal: SetCoachUserMealSchema):
        logger.info(f"[+] Creating Coach User Meal With Coach ID ---> {coach_id}")

        return await self.coach_subservice.create_coach_user_meal(coach_id, meal)
