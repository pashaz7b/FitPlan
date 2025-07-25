# from http.client import responses
# from pyexpat.errors import messages
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
                                            UserRequestMealSchema, GetUserMealSchema,
                                            GetUserAllCoachSchema, UserTakeWorkoutCoachSchema,
                                            UserTakeWorkoutCoachResponseSchema, GroupedExerciseSchema, ExerciseSchema,
                                            ChangeUserCoachResponse)

from app.domain.schemas.user_schema import (UserGetAllVerifiedGymSchema,
                                            UserGetVerifiedGymDetailSchema,
                                            UserGetVerifiedGymCoachesSchema,
                                            UserGetVerifiedGymPlanPriceSchema,
                                            UserGetVerifiedGymCommentsSchema,
                                            CreateUserGymRegistrationSchema,
                                            UserGetGymRegistrationsSchema,
                                            CreateUserGymCommentSchema,
                                            UserGetVerifiedCoachCommentsSchema,
                                            CreateUserCoachCommentSchema,
                                            UserGetCoachPlanPriceSchema)

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
            # id=user.id,
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

    async def user_get_all_verified_gyms(self):
        logger.info("[...] Getting All Verified Gym For User")
        verified_gyms = await self.user_subservice.user_get_all_verified_gyms()

        if not verified_gyms:
            logger.info(f"[-] There is no Verified Gym")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no Verified Gym")

        verified_gyms_list = []
        for verified_gym in verified_gyms:
            verified_gyms_list.append(UserGetAllVerifiedGymSchema(
                gym_id=verified_gym.id,
                gym_name=verified_gym.name,
                gym_location=verified_gym.location
            ))

        return verified_gyms_list

    async def user_get_verified_gym_detail(self, gym_id: int):
        logger.info(f"[...] Getting Verified Gym Detail With Gym ID {gym_id}")

        verified_gym_detail = await self.user_subservice.user_get_verified_gym_detail(gym_id)

        if not verified_gym_detail:
            logger.info(f"[-] There is no Verified Gym Detail For That Gym With Gym ID {gym_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There is no Verified Gym Detail For That Gym")

        verified_gym_detail_response = UserGetVerifiedGymDetailSchema(
            gym_id=verified_gym_detail.id,
            gym_owner_id=verified_gym_detail.owner_id,
            gym_name=verified_gym_detail.name,
            gym_location=verified_gym_detail.location,
            gym_sport_facilities=verified_gym_detail.sport_facilities,
            gym_welfare_facilities=verified_gym_detail.welfare_facilities,
            gym_rating=verified_gym_detail.rating
        )

        return verified_gym_detail_response

    async def user_get_verified_gym_coaches(self, gym_id: int):
        logger.info(f"[...] Getting All Verified Gym With Gym Id {gym_id} Coaches For User")

        verified_gym_coaches = await self.user_subservice.user_get_verified_gym_coaches(gym_id)

        if not verified_gym_coaches:
            logger.info(f"[-] There is no Verified Gym Coaches For That Gym With Gym ID {gym_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There is no Verified Gym Coaches For That Gym")

        verified_gym_coaches_list = []

        for verified_gym_coach in verified_gym_coaches:
            verified_gym_coach_response = UserGetVerifiedGymCoachesSchema(
                work_out_plan_id=verified_gym_coach.present[0].workout_plan_id,
                work_out_plan_name=verified_gym_coach.present[0].workout_plan.name,
                work_out_plan_description=verified_gym_coach.present[0].workout_plan.description,
                work_out_plan_duration_month=verified_gym_coach.present[0].workout_plan.duration_month,
                coach_id=verified_gym_coach.id,
                coach_user_name=verified_gym_coach.user_name,
                coach_name=verified_gym_coach.name,
                coach_email=verified_gym_coach.email,
                coach_phone_number=verified_gym_coach.phone_number,
                coach_gender=verified_gym_coach.gender,
                coach_date_of_birth=verified_gym_coach.date_of_birth,
                coach_height=verified_gym_coach.metrics.height,
                coach_weight=verified_gym_coach.metrics.weight,
                coach_specialization=verified_gym_coach.metrics.specialization,
                coach_biography=verified_gym_coach.metrics.biography,
                coach_status=verified_gym_coach.status,
                coach_rating=verified_gym_coach.metrics.rating,
            )

            verified_gym_coaches_list.append(verified_gym_coach_response)

        return verified_gym_coaches_list

    async def user_get_verified_gym_plan_price(self, gym_id: int):
        logger.info(f"[...] Getting All Verified Gym Plan Price With Gym Id {gym_id} For User")

        verified_gym_plan_prices = await self.user_subservice.user_get_verified_gym_plan_price(gym_id)

        if not verified_gym_plan_prices:
            logger.info(f"[-] There is No Verified Gym Plan Price For That Gym Id {gym_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There Is No Verified Gym Plan Price For That Gym")

        verified_gym_plan_prices_list = []

        for verified_gym_plan_price in verified_gym_plan_prices:
            verified_gym_plan_price_response = UserGetVerifiedGymPlanPriceSchema(
                session_counts=verified_gym_plan_price.session_counts,
                duration_days=verified_gym_plan_price.duration_days,
                is_vip=verified_gym_plan_price.is_vip,
                price=verified_gym_plan_price.price,
            )

            verified_gym_plan_prices_list.append(verified_gym_plan_price_response)

        return verified_gym_plan_prices_list

    async def user_get_verified_gym_comments(self, gym_id: int):
        logger.info(f"[...] Getting All Verified Gym Comments With Gym Id {gym_id} For User")

        verified_gym_comments = await self.user_subservice.user_get_verified_gym_comments(gym_id)

        if not verified_gym_comments:
            logger.info(f"[-] There is No Verified Gym Comments For That Gym Id {gym_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There Is No Verified Gym Comments For That Gym")

        verified_gym_comments_list = []

        for verified_gym_comment in verified_gym_comments:
            verified_gym_comment_response = UserGetVerifiedGymCommentsSchema(
                users_name=verified_gym_comment.user.name,
                comment=verified_gym_comment.comment,
                rating=verified_gym_comment.rating,
                date=verified_gym_comment.date,
            )

            verified_gym_comments_list.append(verified_gym_comment_response)

        return verified_gym_comments_list

    async def create_user_gym_registration(self, user_id: int,
                                           user_gym_registration_schema: CreateUserGymRegistrationSchema):
        logger.info(f"[...] Creating User Gym Registration For User With User ID  {user_id}")

        gym_exists = await self.user_subservice.user_get_verified_gym_detail(user_gym_registration_schema.gym_id)

        if not gym_exists:
            logger.info(f"[-] Gym Not Found With Gym Id {user_gym_registration_schema.gym_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Gym Not Found With Gym Id {user_gym_registration_schema.gym_id}")

        user_gym_registration = await self.user_subservice.get_user_gym_registration_all(user_id)

        if user_gym_registration and user_gym_registration.gym_id:
            logger.info(f"[-] User Already Registered In Gym With Gym Id {user_gym_registration.gym_id}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User Already Registered In Gym")

        return await self.user_subservice.create_user_gym_registration(user_id
                                                                       , user_gym_registration_schema)

    async def get_user_gym_registration_info(self, user_id: int):
        logger.info(f"[...] Getting User Gym Registration Info With Id ---> {user_id}")

        user_gym_registration_info = await self.user_subservice.get_user_gym_registration_info(user_id)

        if not user_gym_registration_info:
            logger.info(f"[-] User's Gym Not Found For User{user_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User's Gym Not Found")

        response = UserGetGymRegistrationsSchema(
            gym_id=user_gym_registration_info.gym_id,
            gym_name=user_gym_registration_info.gym.name,
            registered_sessions=user_gym_registration_info.registered_sessions,
            registered_days=user_gym_registration_info.registered_days,
            is_vip=user_gym_registration_info.is_vip,
            remaining_sessions=user_gym_registration_info.remaining_sessions,
            remaining_days=user_gym_registration_info.remaining_days,
            is_expired=user_gym_registration_info.is_expired,
            date=user_gym_registration_info.date,
        )

        return response

    async def create_user_gym_comment(self, user_id: int,
                                      user_gym_comment_schema: CreateUserGymCommentSchema):
        logger.info(f"[...] Creating user gym comment for user with user_id {user_id}")

        gym_exists = await self.user_subservice.user_get_verified_gym_detail(user_gym_comment_schema.gym_id)

        if not gym_exists:
            logger.info(f"[-] Gym Not Found With Gym Id {user_gym_comment_schema.gym_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Gym Not Found With Gym Id {user_gym_comment_schema.gym_id}")

        if user_gym_comment_schema.rating not in {0, 1, 2, 3, 4, 5}:
            logger.info(f"[-] Invalid rating: {user_gym_comment_schema.rating}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Rating must be an integer between 0 and 5")

        return await self.user_subservice.create_user_gym_comment(user_id, user_gym_comment_schema)

    # ****************************************************************************************

    async def user_get_verified_coach_comments(self, coach_id: int):
        logger.info(f"[...] Getting All Verified Coach Comments With Coach Id {coach_id} For User")

        verified_coach_comments = await self.user_subservice.user_get_verified_coach_comments(coach_id)

        if not verified_coach_comments:
            logger.info(f"[-] There is No Verified Coach Comments For That Coach Id {coach_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There Is No Verified Coach Comments For That Coach")

        verified_coach_comments_list = []

        for verified_coach_comment in verified_coach_comments:
            verified_coach_comment_response = UserGetVerifiedCoachCommentsSchema(
                users_name=verified_coach_comment.user.name,
                comment=verified_coach_comment.comment,
                rating=verified_coach_comment.rating,
                date=verified_coach_comment.date,
            )

            verified_coach_comments_list.append(verified_coach_comment_response)

        return verified_coach_comments_list

    async def create_user_coach_comment(self, user_id: int,
                                        user_coach_comment_schema: CreateUserCoachCommentSchema):
        logger.info(f"[...] Creating user coach comment for user with user_id {user_id}")

        coach_exists = await self.user_subservice.user_get_verified_coach_detail(user_coach_comment_schema.coach_id)

        if not coach_exists:
            logger.info(f"[-] Coach Not Found With Coach Id {user_coach_comment_schema.coach_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Coach Not Found With Coach Id {user_coach_comment_schema.coach_id}")

        if user_coach_comment_schema.rating not in {0, 1, 2, 3, 4, 5}:
            logger.info(f"[-] Invalid rating: {user_coach_comment_schema.rating}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Rating must be an integer between 0 and 5")

        return await self.user_subservice.create_user_coach_comment(user_id, user_coach_comment_schema)

    async def user_get_coach_plan_price(self, user_id: int):
        logger.info(f"[...] Getting Coach Plan Price Associated With Coach For User --> {user_id}")

        users_coach = await self.user_subservice.get_user_coach(user_id)

        if not users_coach:
            logger.info(f"[-] No Coach Found For User --> {user_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Coach Found For User --> {user_id}")

        coach_id = users_coach.id
        coach_plan_price = await self.user_subservice.user_get_coach_plan_price(coach_id)

        if not coach_plan_price:
            logger.info(f"[-] No Plan Price Found For Couch --> {coach_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Plan Price Found For Couch --> {coach_id}")

        coach_plan_price_response = UserGetCoachPlanPriceSchema(
            exercise_price=coach_plan_price.exercise_price,
            meal_price=coach_plan_price.meal_price,
        )

        return coach_plan_price_response
