from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status

from app.domain.schemas.coach_schema import (GetCoachUserSchema, SetCoachUserMealSchema, GetCoachUserMealRequestSchema,
                                             GetCoachUserExerciseRequestSchema, SetCoachUserExerciseSchema,
                                             GetCoachInfoSchema, SetCoachWorkOutPlanSchema, SetCoachInfoSchema,
                                             CoachChangeCoachPlanPriceSchema)

from app.domain.schemas.coach_schema import (CoachGetCoachPlanPriceSchema, CoachCreateCoachPlanPriceSchema,
                                             CoachGetGymPlanPriceSchema,
                                             CoachGetHisGymInfoSchema,
                                             CoachCreateGymPlanPriceSchema, CoachDeleteGymPlanPriceSchema)

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

    async def change_coach_info(self, coach_id: int, coach: SetCoachInfoSchema):
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

        existed_workout_plan = await self.coach_subservice.check_if_workout_plan_exists(coach_id)
        if existed_workout_plan:
            logger.error(f"[-] Workout Plan Already Exists For Coach With ID ---> {coach_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Workout Plan Already Exists For This Coach"
            )

        return await self.coach_subservice.create_workout_plan(coach_id, workout_plan)

    # *******************************************************************************

    async def coach_get_coach_plan_price(self, coach_id: int):
        logger.info(f"[...] Getting Coach Plan Price Associated With Coach For Coach --> {coach_id}")

        coach_plan_price = await self.coach_subservice.coach_get_coach_plan_price(coach_id)

        if not coach_plan_price:
            logger.info(f"[-] No Plan Price Found For Couch --> {coach_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Plan Price Found For Couch --> {coach_id}")

        coach_plan_price_response = CoachGetCoachPlanPriceSchema(
            exercise_price=coach_plan_price.exercise_price,
            meal_price=coach_plan_price.meal_price,
        )

        return coach_plan_price_response

    async def coach_create_coach_plan_price(self, coach_id: int,
                                            coach_plan_price_schema: CoachCreateCoachPlanPriceSchema):
        logger.info(f"[...] Creating Coach Plan Price For Coach With Id ---> {coach_id}")

        coach_plan_price_exists = await self.coach_subservice.coach_get_coach_plan_price(coach_id)

        if coach_plan_price_exists:
            logger.info("Coach Plan Price Already Exists")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Coach Plan Price Already Exists")

        return await self.coach_subservice.coach_create_coach_plan_price(coach_id, coach_plan_price_schema)

    async def coach_change_coach_plan_price(self, coach_id: int,
                                            coach_plan_price_schema: CoachChangeCoachPlanPriceSchema):
        current_coach_plan_price_response = await self.coach_subservice.coach_get_coach_plan_price(coach_id)

        if not current_coach_plan_price_response:
            logger.info(f"No Coach Plan Price Found For Couch --> {coach_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Coach Plan Price Found")

        coach_plan_price_schema_dict = {"exercise_price": coach_plan_price_schema.exercise_price,
                                        "meal_price": coach_plan_price_schema.meal_price}

        return await self.coach_subservice.coach_change_coach_plan_price(coach_id, coach_plan_price_schema_dict)

    async def coach_get_gym_plan_price(self, coach_id: int, gym_id: int):
        logger.info(f"[...] Getting Verified Gym Plan Prices For Coach With Id {coach_id}")

        verified_gym_plan_prices = await self.coach_subservice.coach_get_gym_plan_price(coach_id, gym_id)

        if not verified_gym_plan_prices:
            logger.info(f"[-] There is No Gym Plan Price")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There Is No Verified Gym Plan Price")

        verified_gym_plan_prices_list = []

        for verified_gym_plan_price in verified_gym_plan_prices:
            verified_gym_plan_price_response = CoachGetGymPlanPriceSchema(
                plan_price_id=verified_gym_plan_price.id,
                session_counts=verified_gym_plan_price.session_counts,
                duration_days=verified_gym_plan_price.duration_days,
                is_vip=verified_gym_plan_price.is_vip,
                price=verified_gym_plan_price.price,
            )

            verified_gym_plan_prices_list.append(verified_gym_plan_price_response)

        return verified_gym_plan_prices_list

    async def coach_get_his_gym_info(self, coach_id: int):
        logger.info(f"[...] Getting gym info for Coach With Id {coach_id}")

        gyms_for_coach = await self.coach_subservice.coach_get_his_gym_info(coach_id)

        if not gyms_for_coach:
            logger.info(f"No Gym Info Found For Coach With Id {coach_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Gym Info Found")

        gym_list = []

        for gym in gyms_for_coach:
            gym_info = CoachGetHisGymInfoSchema(
                gym_id=gym.id,
                gym_name=gym.name
            )
            gym_list.append(gym_info)

        return gym_list

    async def coach_create_gym_plan_price(self, coach_id: int, gym_id: int,
                                          verified_gym_plan_price_schema: CoachCreateGymPlanPriceSchema):
        logger.info(f"[...] Creating Gym Plan Price For Gym With Id ---> {gym_id}")

        gym_info = await self.coach_subservice.get_gym_info(gym_id)

        if not gym_info:
            logger.error(f"[-] No Gym Found With Id {gym_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Gym Found")

        gym_owner_id = gym_info.owner_id

        if gym_owner_id != coach_id:
            logger.error(f"[-] Coach With Id {coach_id} Is Not The Owner Of Gym With Id {gym_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You Are Not Authorized To Create Gym Plan Price"
            )

        return await self.coach_subservice.coach_create_gym_plan_price(gym_id, verified_gym_plan_price_schema)

    async def coach_delete_gym_plan_price(self, coach_id: int, plan_price_schema: CoachDeleteGymPlanPriceSchema):
        plan_price_id = plan_price_schema.plan_price_id
        logger.info(f"[...] Deleting Gym Plan Price With Id ---> {plan_price_id}")

        gym_plan_price = await self.coach_subservice.check_plan_price_exists_and_valid(plan_price_id)

        if not gym_plan_price:
            logger.error(f"[-] No Gym Plan Price Found With Id {plan_price_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Gym Plan Price Found")

        gym_plan_price_gym_id = gym_plan_price.gym_id

        gym_info = await self.coach_subservice.get_gym_info(gym_plan_price_gym_id)

        if not gym_info:
            logger.error(f"[-] No Gym Found With Id {gym_plan_price_gym_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Gym Found")

        gym_owner_id = gym_info.owner_id

        if gym_owner_id != coach_id:
            logger.error(f"[-] Coach With Id {coach_id} Is Not The Owner Of Gym Plan Price With Id {plan_price_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You Are Not Authorized To Delete This Gym Plan Price"
            )

        return await self.coach_subservice.coach_delete_gym_plan_price(plan_price_schema)
