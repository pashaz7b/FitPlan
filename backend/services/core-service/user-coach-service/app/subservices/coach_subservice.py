from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends

from app.domain.models.fitplan_model import (Coach,
                                             CoachMetrics, MealSupplement, UserMealMealSupplement,
                                             WorkoutPlanMealSupplement)
from app.domain.schemas.coach_schema import SetCoachUserMealSchema, SetCoachUserMealResponseSchema
from app.infrastructure.repositories.coach_repository import CoachRepository
from app.subservices.auth.hash_subservice import HashService
from app.subservices.baseconfig import BaseService


class CoachSubService(BaseService):
    def __init__(self,
                 coach_repo: Annotated[CoachRepository, Depends()],
                 hash_subservice: Annotated[HashService, Depends()]
                 ) -> None:
        super().__init__()
        self.coach_repo = coach_repo
        self.hash_subservice = hash_subservice

    # async def create_coach(self, coach_struct: CoachRegisterSchema) -> Coach:
    #     logger.info(f"[+] Creating Coach With Email ---> {coach_struct.email}")
    #     new_coach = Coach(
    #         password=self.hash_subservice.hash_password(coach_struct.password),
    #         user_name=coach_struct.user_name,
    #         name=coach_struct.name,
    #         email=coach_struct.email,
    #         phone_number=coach_struct.phone_number,
    #         gender=coach_struct.gender,
    #         date_of_birth=coach_struct.date_of_birth,
    #     )
    #
    #     created_coach = self.coach_repo.create_coach(new_coach)
    #
    #     coach_metrics = CoachMetrics(
    #         coach_id=created_coach.id,
    #         height=coach_struct.height,
    #         weight=coach_struct.weight,
    #         specialization=coach_struct.specialization,
    #         biography=coach_struct.biography
    #     )
    #     self.coach_repo.create_coach_metrics(coach_metrics)
    #
    #     return created_coach

    async def update_coach(self, coach_id: int, update_fields: Dict) -> Coach:
        logger.info(f"Updating coach with id {coach_id}")
        return self.coach_repo.update_coach(coach_id, update_fields)

    async def update_coach_by_email(self, email: str, update_fields: Dict) -> Coach:
        logger.info(f"Updating coach with Email ---> {email}")
        return self.coach_repo.update_coach_by_email(email, update_fields)

    async def delete_coach(self, coach: Coach) -> None:
        logger.info(f"Deleting coach with id {coach.id}")
        return self.coach_repo.delete_coach(coach)

    async def get_coach(self, coach_id: int) -> Coach:
        logger.info(f"Fetching coach with id {coach_id}")
        return self.coach_repo.get_coach(coach_id)

    async def get_coach_by_email(self, email: str) -> Coach:
        logger.info(f"[+] Fetching coach with Email ---> {email}")
        return self.coach_repo.get_coach_by_email(email)

    async def get_coach_user(self, coach_id: int):
        logger.info(f"Fetching coach user with coach_id {coach_id}")
        return self.coach_repo.get_coach_user(coach_id)

    async def get_coach_user_meal_request(self, coach_id: int):
        logger.info(f"Fetching coach user meal request with coach_id {coach_id}")
        return self.coach_repo.get_coach_user_meal_request(coach_id)
        # all_user_meal = self.coach_repo.get_coach_user_meal_request(coach_id)
        # all_user_meal_supplements = self.coach_repo.get_user_meal_meal_supplement()
        # supplement_user_meal_ids = {supplement.user_meal_id for supplement in all_user_meal_supplements}
        #
        # filtered_user_meals = []
        # for user in all_user_meal:
        #     for request_meal in user.user_request_meals:
        #         if request_meal.user_meal.id not in supplement_user_meal_ids:
        #             filtered_user_meals.append(user)
        #             break
        #
        # logger.info(f"Filtered user meals: {filtered_user_meals}")
        # return all_user_meal

    async def create_coach_user_meal(self, coach_id: int, meal: SetCoachUserMealSchema):
        logger.info(f"Creating coach user meal with coach_id {coach_id}")

        meal_supplement = MealSupplement(
            breakfast=meal.breakfast,
            lunch=meal.lunch,
            dinner=meal.dinner,
            supplement=meal.supplement,
            expire_time=meal.expire_time
        )

        created_meal_supplement = self.coach_repo.create_meal_supplement(meal_supplement)

        user_meal_meal_supplement = UserMealMealSupplement(
            user_meal_id=meal.user_meal_id,
            meal_supplement_id=created_meal_supplement.id
        )

        self.coach_repo.create_user_meal_meal_supplement(user_meal_meal_supplement)

        workout_plan_meal_supplement = WorkoutPlanMealSupplement(
            workout_plan_id=meal.work_out_plan_id,
            meal_supplement_id=created_meal_supplement.id
        )

        self.coach_repo.create_work_out_plan_meal_supplement(workout_plan_meal_supplement)

        return SetCoachUserMealResponseSchema(
            meal_id=created_meal_supplement.id,
            message="Meal Created Successfully"
        )

    async def get_is_answered_requested_meal(self, user_meal_id: int):
        return self.coach_repo.get_is_answered_requested_meal(user_meal_id)
