import jdatetime

from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends

from app.domain.models.fitplan_model import (User,
                                             UserExercise,
                                             UserRequestExercise, TransactionLog, UserTransactionLog,
                                             UserMeal, UserRequestMeal,
                                             Take)
from app.domain.models.fitplan_model import UserMetrics
from app.domain.schemas.user_schema import (UserRequestExerciseSchema,
                                            UserRequestExerciseResponseSchema, SetUserTransactionsSchema,
                                            UserRequestMealSchema, UserRequestMealResponseSchema,
                                            UserTakeWorkoutCoachSchema)
from app.infrastructure.repositories.user_repository import UserRepository
from app.subservices.auth.hash_subservice import HashService
from app.subservices.baseconfig import BaseService


class UserSubService(BaseService):
    def __init__(self,
                 user_repo: Annotated[UserRepository, Depends()],
                 hash_subservice: Annotated[HashService, Depends()]
                 ) -> None:
        super().__init__()
        self.user_repo = user_repo
        self.hash_subservice = hash_subservice

    # async def create_user(self, user_struct: UserRegisterSchema) -> User:
    #     logger.info(f"[+] Creating User With Email ---> {user_struct.email}")
    #
    #     new_user = User(password=self.hash_subservice.hash_password(user_struct.password),
    #                     user_name=user_struct.user_name,
    #                     name=user_struct.name,
    #                     email=user_struct.email,
    #                     phone_number=user_struct.phone_number,
    #                     gender=user_struct.gender,
    #                     date_of_birth=user_struct.date_of_birth)
    #
    #     created_user = self.user_repo.create_user(new_user)
    #
    #     user_metrics = UserMetrics(
    #         user_id=created_user.id,
    #         height=user_struct.height,
    #         weight=user_struct.weight,
    #         # waist=user_struct.waist,
    #         # injuries=user_struct.injuries,
    #     )
    #     self.user_repo.create_user_metrics(user_metrics)
    #
    #     return new_user

    async def update_user(self, user_id: int, update_fields: Dict) -> User:
        logger.info(f"Updating user with id {user_id}")
        return self.user_repo.update_user(user_id, update_fields)

    async def update_user_by_email(self, email: str, update_fields: Dict) -> User:
        logger.info(f"Updating user with Email ---> {email}")
        return self.user_repo.update_user_by_email(email, update_fields)

    async def delete_user(self, user: User) -> None:
        logger.info(f"Deleting user with id {user.id}")
        return self.user_repo.delete_user(user)

    async def get_user(self, user_id: int) -> User:
        logger.info(f"Fetching user with id {user_id}")
        return self.user_repo.get_user(user_id)

    async def get_user_metrics(self, user_id: int):
        logger.info(f"Fetching user metrics with user_id {user_id}")
        return self.user_repo.get_user_metrics(user_id)

    async def get_user_by_email(self, email: str) -> User:
        logger.info(f"[+] Fetching user with Email ---> {email}")
        return self.user_repo.get_user_by_email(email)

    async def change_user_info(self, user_id: int, changes: Dict) -> None:
        logger.info(f"Updating user with id {user_id} with changes: {changes}")

        user_changes = {}
        metrics_changes = {}

        for key, value in changes.items():
            if key in {"password", "user_name", "name", "email", "phone_number", "gender", "date_of_birth"}:
                user_changes[key] = value
            elif key in {"height", "weight"}:
                metrics_changes[key] = value

        if user_changes:
            logger.info(f"Applying user updates: {user_changes}")
            self.user_repo.update_user(user_id, user_changes)

        if metrics_changes:
            logger.info(f"Applying user metrics updates: {metrics_changes}")
            self.user_repo.update_user_metrics(user_id, metrics_changes)

        logger.info(f"User with id {user_id} updated successfully")

    async def get_user_transaction_log(self, user_id: int):
        logger.info(f"Fetching user transactions with user_id {user_id}")
        return self.user_repo.get_user_transaction_log(user_id)

    async def create_transaction_log(self, user_id: int, transaction_schema: SetUserTransactionsSchema):
        logger.info(f"Creating transaction log for user with user_id {user_id}")

        transaction = TransactionLog(
            amount=transaction_schema.amount,
            reason=transaction_schema.reason,
            status=transaction_schema.status,
            date=transaction_schema.date
        )

        self.user_repo.create_transaction_log(transaction)

        user_transaction_log = UserTransactionLog(
            user_id=user_id,
            transaction_id=transaction.id
        )

        self.user_repo.create_user_transaction_log(user_transaction_log)

        return transaction

    async def get_user_coach(self, user_id: int):
        logger.info(f"Fetching user coach with user_id {user_id}")
        return self.user_repo.get_user_coach(user_id)

    async def create_user_exercise(self, user_id, user_struct: UserRequestExerciseSchema):
        logger.info(f"Creating user request exercise with user_id {user_id}")

        exercise = UserExercise(
            weight=user_struct.weight,
            waist=user_struct.waist,
            type=user_struct.type,
            price=self.config.FitPlAN_PRICE
        )

        created_exercise = self.user_repo.create_user_exercise(exercise)

        user_request_exercise = UserRequestExercise(
            user_id=user_id,
            user_exercise_id=created_exercise.id
        )

        self.user_repo.create_user_request_exercise(user_request_exercise)

        transaction = SetUserTransactionsSchema(amount=self.config.FitPlAN_PRICE,
                                                reason="Exercise",
                                                status="Success",
                                                date=jdatetime.date.today().strftime("%Y/%m/%d"))

        await self.create_transaction_log(user_id, transaction)

        return UserRequestExerciseResponseSchema(
            weight=created_exercise.weight,
            waist=created_exercise.waist,
            type=created_exercise.type,
            price=created_exercise.price,
            msg="Request Exercise created successfully"
        )

    async def get_user_exercise(self, user_id: int):
        logger.info(f"Fetching user exercise with user_id {user_id}")
        return self.user_repo.get_user_exercise(user_id)

    async def create_user_meal(self, user_id, user_struct: UserRequestMealSchema):
        logger.info(f"Creating user request meal with user_id {user_id}")

        meal = UserMeal(
            weight=user_struct.weight,
            waist=user_struct.waist,
            type=user_struct.type,
            price=self.config.FitPlAN_PRICE
        )

        created_meal = self.user_repo.create_user_meal(meal)

        user_request_meal = UserRequestMeal(
            user_id=user_id,
            user_meal_id=created_meal.id
        )

        self.user_repo.create_user_request_meal(user_request_meal)

        transaction = SetUserTransactionsSchema(amount=self.config.FitPlAN_PRICE,
                                                reason="Meal",
                                                status="Success",
                                                date=jdatetime.date.today().strftime("%Y/%m/%d"))

        await self.create_transaction_log(user_id, transaction)

        return UserRequestMealResponseSchema(
            weight=created_meal.weight,
            waist=created_meal.waist,
            type=created_meal.type,
            price=created_meal.price,
            msg="Request Meal created successfully"
        )

    async def get_user_meal(self, user_id: int):
        logger.info(f"Fetching user meal with user_id {user_id}")
        return self.user_repo.get_user_meal(user_id)

    async def get_user_all_coach(self, user_id: int):
        logger.info(f"[...] Getting all coaches for user {user_id}")
        return self.user_repo.get_user_all_coach(user_id)

    async def create_user_take_workout_coach(self, user_id: int, take_struct: UserTakeWorkoutCoachSchema):
        logger.info(f"[...] Creating user take workout coach for user {user_id}")

        take = Take(
            user_id=user_id,
            workout_plan_id=take_struct.work_out_plan_id
        )

        return self.user_repo.create_user_take_workout_coach(take)

