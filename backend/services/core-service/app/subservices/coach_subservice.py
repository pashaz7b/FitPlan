from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends

from app.domain.models.fitplan_model import (Coach,
                                             CoachMetrics, MealSupplement, UserMealMealSupplement,
                                             WorkoutPlanMealSupplement, Exercise, UserExerciseExercise,
                                             WorkoutPlanExercise, WorkoutPlan, Present, CoachPlanPrice, GymPlanPrice)

from app.domain.schemas.coach_schema import (SetCoachUserMealSchema, SetCoachUserMealResponseSchema,
                                             SetCoachUserExerciseSchema, SetCoachUserExerciseResponseSchema,
                                             SetCoachWorkOutPlanSchema,
                                             SetCoachWorkOutPlanResponseSchema, CoachCreateCoachPlanPriceSchema,
                                             CoachCreateCoachPlanPriceResponseSchema,
                                             CoachChangeCoachPlanPriceResponseSchema,
                                             CoachCreateGymPlanPriceSchema,
                                             CoachCreateGymPlanPriceResponseSchema,
                                             CoachDeleteGymPlanPriceSchema, CoachDeleteGymPlanPriceResponseSchema,
                                             CoachChangeGymPlanPriceResponseSchema)

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

    async def get_coach_metrics(self, coach_id: int):
        logger.info(f"Fetching coach metrics with coach_id {coach_id}")
        return self.coach_repo.get_coach_metrics(coach_id)

    async def get_coach_by_email(self, email: str) -> Coach:
        logger.info(f"[+] Fetching coach with Email ---> {email}")
        return self.coach_repo.get_coach_by_email(email)

    async def change_coach_info(self, coach_id: int, changes: Dict) -> None:
        logger.info(f"Updating coach with id {coach_id} with changes: {changes}")

        coach_changes = {}
        metrics_changes = {}

        for key, value in changes.items():
            if key in ["password", "user_name", "name", "email", "phone_number", "gender", "status", "date_of_birth"]:
                coach_changes[key] = value
            elif key in ["height", "weight", "specialization", "biography"]:
                metrics_changes[key] = value

        if coach_changes:
            logger.info(f"Applying coach updates: {coach_changes}")
            self.coach_repo.update_coach(coach_id, coach_changes)

        if metrics_changes:
            logger.info(f"Applying coach metrics updates: {metrics_changes}")
            self.coach_repo.update_coach_metrics(coach_id, metrics_changes)

        logger.info(f"Coach updated successfully")

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

    async def get_coach_user_exercise_request(self, coach_id: int):
        logger.info(f"Fetching coach user exercise request with coach_id {coach_id}")
        return self.coach_repo.get_coach_user_exercise_request(coach_id)

    async def get_is_answered_requested_exercise(self, user_exercise_id: int):
        return self.coach_repo.get_is_answered_requested_exercise(user_exercise_id)

    async def create_coach_user_exercise(self, coach_id: int, user_exercise_id: int, work_out_plan_id: int,
                                         exercises: list[SetCoachUserExerciseSchema]):
        logger.info(f"creating coach user exercise with coach_id {coach_id}")

        exercise_ids = []

        for exercise in exercises:
            exercise_sql = Exercise(
                day=exercise.day,
                name=exercise.name,
                set=exercise.set,
                expire_time=exercise.expire_time
            )

            created_exercise_sql = self.coach_repo.create_exercise(exercise_sql)
            exercise_ids.append(created_exercise_sql.id)

        for exercise_id in exercise_ids:
            user_exercise_exercise = UserExerciseExercise(
                user_exercise_id=user_exercise_id,
                exercise_id=exercise_id
            )
            self.coach_repo.create_user_exercise_exercise(user_exercise_exercise)

        for exercise_id in exercise_ids:
            workout_plan_exercise = WorkoutPlanExercise(
                workout_plan_id=work_out_plan_id,
                exercise_id=exercise_id
            )
            self.coach_repo.create_workout_plan_exercise(workout_plan_exercise)

        return SetCoachUserExerciseResponseSchema(
            message="Exercise Created Successfully"
        )

    async def create_workout_plan(self, coach_id: int, workout_plan: SetCoachWorkOutPlanSchema):
        logger.info(f"[+] Creating workout plan For Coach With id {coach_id}")

        the_workout_plan = WorkoutPlan(
            name=workout_plan.workout_plan_name,
            description=workout_plan.workout_plan_description,
            duration_month=workout_plan.workout_plan_duration_month
        )

        created_workout_plan = self.coach_repo.create_workout_plan(the_workout_plan)

        present = Present(
            coach_id=coach_id,
            workout_plan_id=created_workout_plan.id
        )

        self.coach_repo.create_present(present)

        return SetCoachWorkOutPlanResponseSchema(
            workout_plan_id=created_workout_plan.id,
            message="Exercise Created Successfully"
        )

    async def check_if_workout_plan_exists(self, coach_id: int):
        logger.info(f"[+] Checking If Workout Plan Exists for Coach With Id ---> {coach_id}")
        return self.coach_repo.check_if_workout_plan_exists(coach_id)

    async def coach_get_coach_plan_price(self, coach_id: int):
        logger.info(f"[...] Getting Coach Plan Price Association With Coach --> {coach_id}")
        return self.coach_repo.coach_get_coach_plan_price(coach_id)

    async def coach_create_coach_plan_price(self, coach_id: int,
                                            coach_plan_price_schema: CoachCreateCoachPlanPriceSchema):
        logger.info(f"Creating Coach Plan Price For Coach With Id ---> {coach_id}")

        coach_plan_price_model = CoachPlanPrice(
            coach_id=coach_id,
            exercise_price=coach_plan_price_schema.exercise_price,
            meal_price=coach_plan_price_schema.meal_price,
        )

        created_coach_plan_price = self.coach_repo.coach_create_coach_plan_price(coach_plan_price_model)

        response = CoachCreateCoachPlanPriceResponseSchema(
            created_coach_plan_price_id=created_coach_plan_price.id,
            message="Coach Plan Price Created Successfully"
        )

        return response

    async def coach_change_coach_plan_price(self, coach_id: int, coach_plan_price_schema_dict: Dict):
        logger.info(f"Updating Coach Plan Price For Coach With Id ---> {coach_id}")
        self.coach_repo.coach_update_coach_plan_price(coach_id, coach_plan_price_schema_dict)
        response = CoachChangeCoachPlanPriceResponseSchema(
            message="Coach Plan Price Updated Successfully"
        )

        return response

    async def coach_get_gym_plan_price(self, coach_id: int, gym_id: int):
        logger.info(f"Getting Gym Plan for Coach With Id ---> {coach_id}")
        return self.coach_repo.coach_get_verified_gym_plan_price(coach_id, gym_id)

    async def coach_get_his_gym_info(self, coach_id: int):
        logger.info(f"Getting gym info for Coach With Id ---> {coach_id}")
        return self.coach_repo.coach_get_his_gym_info(coach_id)

    async def get_gym_info(self, gym_id: int):
        logger.info(f"Getting gym info for Gym With Id ---> {gym_id}")
        return self.coach_repo.get_gym_info(gym_id)

    async def coach_create_gym_plan_price(self, gym_id: int,
                                          verified_gym_plan_price_schema: CoachCreateGymPlanPriceSchema):
        logger.info(f"Creating Gym Plan Price For Gym With Id ---> {gym_id}")

        gym_plan_price_model = GymPlanPrice(
            gym_id=gym_id,
            session_counts=verified_gym_plan_price_schema.session_counts,
            duration_days=verified_gym_plan_price_schema.duration_days,
            is_vip=verified_gym_plan_price_schema.is_vip,
            price=verified_gym_plan_price_schema.price
        )

        created_plan_price = self.coach_repo.coach_create_verified_gym_plan_price(gym_plan_price_model)

        response = CoachCreateGymPlanPriceResponseSchema(
            plan_price_id=created_plan_price.id,
            message="Gym Plan Price Created Successfully"
        )

        return response

    async def check_plan_price_exists_and_valid(self, plan_price_id: int):
        logger.info(f"Checking if Gym Plan Price Exists and Valid With Id ---> {plan_price_id}")
        return self.coach_repo.check_plan_price_exists_and_valid(plan_price_id)

    async def coach_delete_gym_plan_price(self, plan_price_schema: CoachDeleteGymPlanPriceSchema):
        logger.info(f"Deleting Gym Plan Price With Plan Price Id ---> {plan_price_schema.plan_price_id}")
        self.coach_repo.coach_delete_gym_plan_price(plan_price_schema.plan_price_id)

        response = CoachDeleteGymPlanPriceResponseSchema(
            message="Gym Plan Price Deleted Successfully"
        )

        return response

    async def coach_update_gym_plan_price(self, plan_price_id: int,
                                          verified_gym_plan_price_schema_dict: Dict):
        logger.info(f"Updating Gym Plan Price with gym_plan_price_id ---> {plan_price_id}")
        self.coach_repo.coach_update_gym_plan_price(plan_price_id, verified_gym_plan_price_schema_dict)
        response = CoachChangeGymPlanPriceResponseSchema(
            message="Gym Plan Price Updated Successfully"
        )
        return response
