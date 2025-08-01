from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.core.postgres_db.postgres_database import get_db
from app.domain.models.fitplan_model import (User,
                                             UserMetrics,
                                             TransactionLog,
                                             UserTransactionLog,
                                             Coach,
                                             Take,
                                             Present,
                                             WorkoutPlan,
                                             UserExercise,
                                             UserRequestExercise, UserExerciseExercise, Exercise, UserMeal,
                                             UserRequestMeal, MealSupplement, UserMealMealSupplement,
                                             WorkoutPlanExercise, WorkoutPlanMealSupplement, CoachPlanPrice)

from app.domain.models.fitplan_model import (Gym, CoachGym,
                                             GymPlanPrice, GymComment,
                                             UserGymRegistration, CoachComment,
                                             CoachMetrics)


class UserRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        logger.info(f"[+] User Created With Id ---> {user.id} And Email ---> {user.email}")
        return user

    def create_user_metrics(self, metrics: UserMetrics) -> UserMetrics:
        self.db.add(metrics)
        self.db.commit()
        self.db.refresh(metrics)
        logger.info(f"[+] Metrics Created For Coach Id ---> {metrics.user_id}")
        return metrics

    def update_user(self, user_id: int, updated_user: Dict):
        user_query = self.db.query(User).filter(User.id == user_id)
        db_user = user_query.first()
        user_query.filter(User.id == user_id).update(
            updated_user, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"[+] User With Id ---> {user_id} Updated")
        return db_user

    def update_user_metrics(self, user_id: int, updated_metrics: Dict):
        metrics_query = self.db.query(UserMetrics).filter(UserMetrics.user_id == user_id)
        db_metrics = metrics_query.first()
        metrics_query.filter(UserMetrics.user_id == user_id).update(
            updated_metrics, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_metrics)
        logger.info(f"[+] Metrics For User With Id ---> {user_id} Updated")
        return db_metrics

    def update_user_by_email(self, user_email: str, updated_user: Dict):
        user_query = self.db.query(User).filter(User.email == user_email)
        db_user = user_query.first()
        user_query.filter(User.email == user_email).update(
            updated_user, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"[+] User With Email ---> {user_email} Updated")
        return db_user

    def delete_user(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
        self.db.flush()
        logger.info(f"[+] User Deleted With Id ---> {user.id} And Email ---> {user.email}")

    def get_user(self, user_id: int):
        logger.info(f"[+] Fetching User With Id ---> {user_id}")
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_metrics(self, user_id: int):
        logger.info(f"[+] Fetching Metrics For User With Id ---> {user_id}")
        return self.db.query(UserMetrics).filter(UserMetrics.user_id == user_id).first()

    def get_user_by_email(self, email: str):
        logger.info(f"[+] Fetching User With Email --> {email}")
        return self.db.query(User).filter(User.email == email).first()

    def get_user_transaction_log(self, user_id: int):
        logger.info(f"[+] Fetching Transaction Log For User With Id ---> {user_id}")
        return (
            self.db.query(TransactionLog)
            .join(UserTransactionLog, TransactionLog.id == UserTransactionLog.transaction_id)
            .filter(UserTransactionLog.user_id == user_id)
            .all()
        )

    def create_transaction_log(self, transaction_log: TransactionLog) -> TransactionLog:
        self.db.add(transaction_log)
        self.db.commit()
        self.db.refresh(transaction_log)
        logger.info(f"[+] Transaction Log Created With Id ---> {transaction_log.id}")
        return transaction_log

    def create_user_transaction_log(self, user_transaction_log: UserTransactionLog) -> UserTransactionLog:
        self.db.add(user_transaction_log)
        self.db.commit()
        self.db.refresh(user_transaction_log)
        logger.info(f"[+] User Transaction Log Created With User Id ---> {user_transaction_log.user_id}")
        return user_transaction_log

    def get_user_coach(self, user_id: int):
        logger.info(f"[+] Fetching Coach for User With Id ---> {user_id}")
        coach = (
            self.db.query(Coach)
            .join(Present, Coach.id == Present.coach_id)
            .join(WorkoutPlan, Present.workout_plan_id == WorkoutPlan.id)
            .join(Take, WorkoutPlan.id == Take.workout_plan_id)
            .join(User, Take.user_id == User.id)  # Join Take with User using user_id
            .filter(User.id == user_id)  # Ensure we filter by the user_id
            .first()  # Get the first result (assuming only one coach per user)
        )

        return coach

    def create_user_exercise(self, user_exercise: UserExercise) -> UserExercise:
        self.db.add(user_exercise)
        self.db.commit()
        self.db.refresh(user_exercise)
        logger.info(f"[+] User Exercise Created With Id ---> {user_exercise.id}")
        return user_exercise

    def create_user_request_exercise(self, user_request_exercise: UserRequestExercise) -> UserRequestExercise:
        self.db.add(user_request_exercise)
        self.db.commit()
        self.db.refresh(user_request_exercise)
        logger.info(f"[+] User Request Exercise Created With User Id ---> {user_request_exercise.user_id}")
        return user_request_exercise

    def get_user_exercise(self, user_id: int):
        logger.info(f"[+] Fetching User Exercise For User With Id ---> {user_id}")
        fetched_exercise = (
            self.db.query(Exercise)
            .join(WorkoutPlanExercise, Exercise.id == WorkoutPlanExercise.exercise_id)
            .join(WorkoutPlan, WorkoutPlanExercise.workout_plan_id == WorkoutPlan.id)
            .join(Present, WorkoutPlan.id == Present.workout_plan_id)
            .join(Coach, Present.coach_id == Coach.id)
            .join(UserExerciseExercise, Exercise.id == UserExerciseExercise.exercise_id)
            .join(UserExercise, UserExerciseExercise.user_exercise_id == UserExercise.id)
            .join(UserRequestExercise, UserExercise.id == UserRequestExercise.user_exercise_id)
            .join(User, UserRequestExercise.user_id == User.id)
            .filter(User.id == user_id)
            .all()
        )
        return fetched_exercise

    def create_user_meal(self, user_meal: UserMeal):
        self.db.add(user_meal)
        self.db.commit()
        self.db.refresh(user_meal)
        logger.info(f"[+] User Meal Created With Id ---> {user_meal.id}")
        return user_meal

    def create_user_request_meal(self, user_meal_request: UserRequestMeal):
        self.db.add(user_meal_request)
        self.db.commit()
        self.db.refresh(user_meal_request)
        logger.info(f"[+] User Meal Request Created With Id ---> {user_meal_request.user_id}")
        return user_meal_request

    def get_user_meal(self, user_id: int):
        logger.info(f"[+] Fetching User Meal For User With Id ---> {user_id}")

        fetched_meal = (
            self.db.query(MealSupplement)
            .join(WorkoutPlanMealSupplement, MealSupplement.id == WorkoutPlanMealSupplement.meal_supplement_id)
            .join(WorkoutPlan, WorkoutPlanMealSupplement.workout_plan_id == WorkoutPlan.id)
            .join(Present, WorkoutPlan.id == Present.workout_plan_id)
            .join(Coach, Present.coach_id == Coach.id)
            .join(UserMealMealSupplement, MealSupplement.id == UserMealMealSupplement.meal_supplement_id)
            .join(UserMeal, UserMealMealSupplement.user_meal_id == UserMeal.id)
            .join(UserRequestMeal, UserMeal.id == UserRequestMeal.user_meal_id)
            .join(User, UserRequestMeal.user_id == User.id)
            .filter(User.id == user_id)
            .all()
        )
        return fetched_meal

    def get_user_all_coach(self, user_id: int):
        logger.info(f"[+] Fetching All Coach for User With Id ---> {user_id}")
        # ready_coaches = (
        #     self.db.query(Coach)
        #     .join(Present, Coach.id == Present.coach_id)
        #     .join(WorkoutPlan, Present.workout_plan_id == WorkoutPlan.id)
        #     .filter(Coach.status == True)
        #     .all()
        # )
        ready_coaches = (
            self.db.query(Coach)
            .options(joinedload(Coach.present).joinedload(Present.workout_plan))
            .filter(Coach.status == True)
            .filter(Coach.verification_status == "verified")
            .all()
        )

        return ready_coaches

    def create_user_take_workout_coach(self, take: Take) -> Take:
        self.db.add(take)
        self.db.commit()
        self.db.refresh(take)
        logger.info(f"[+] User Take Workout Coach Created With Id ---> {take.user_id}")
        return take

    def update_user_coach(self, user_id: int, updated_user: Dict):
        user_query = self.db.query(Take).filter(Take.user_id == user_id)
        db_user = user_query.first()
        user_query.filter(Take.user_id == user_id).update(
            updated_user, synchronize_session=False
        )
        self.db.commit()
        logger.info(f"[+] User With Id ---> {user_id} Updated")
        return db_user

    def check_if_user_take_workout_coach_exists(self, user_id: int):
        logger.info(f"[+] Checking If User Take Workout Coach Exists For User With Id ---> {user_id}")
        return self.db.query(Take).filter(Take.user_id == user_id).first()

    def user_get_all_verified_gyms(self):
        logger.info(f"[+] Fetching All Verified Gyms")

        verified_gyms = (
            self.db.query(Gym)
            .filter(Gym.verification_status == "verified")
            .all()
        )

        return verified_gyms

    def user_get_verified_gym_detail(self, gym_id: int):
        logger.info(f"[+] Fetching Verified Gym Detail With Gym Id ---> {gym_id}")

        verified_gym_detail = (
            self.db.query(Gym)
            .filter(Gym.verification_status == "verified")
            .filter(Gym.id == gym_id)
            .first()
        )

        return verified_gym_detail

    def user_get_verified_gym_coaches(self, gym_id: int):
        logger.info(f"[+] Fetching Verified Gym Coaches With Gym Id ---> {gym_id}")

        verified_gym_coaches = (
            self.db.query(Coach)
            .filter(Coach.verification_status == "verified")
            .filter(Coach.status == True)
            .filter(Coach.is_verified == True)
            .join(CoachGym, Coach.id == CoachGym.coach_id)
            .filter(CoachGym.gym_id == gym_id)
            .join(Gym, CoachGym.gym_id == Gym.id)
            .filter(Gym.verification_status == "verified")
            .join(Present, Coach.id == Present.coach_id)
            .all()
        )

        return verified_gym_coaches

    def user_get_verified_gym_plan_price(self, gym_id: int):
        logger.info(f"[+] Fetching Verified Gym Plan Price With Id ---> {gym_id}")

        verified_gym_plan_price = (
            self.db.query(GymPlanPrice)
            .join(Gym, GymPlanPrice.gym_id == Gym.id)
            .filter(Gym.id == gym_id)
            .filter(Gym.verification_status == "verified")
            .all()
        )

        return verified_gym_plan_price

    def user_get_verified_gym_comments(self, gym_id: int):
        logger.info(f"[+] Fetching Verified Gym Comments With Id ---> {gym_id}")

        verified_gym_comments = (
            self.db.query(GymComment)
            .filter(GymComment.gym_id == gym_id)
            .join(Gym, GymComment.gym_id == Gym.id)
            .filter(Gym.verification_status == "verified")
            .all()
        )

        return verified_gym_comments

    def get_user_gym_registration_all(self, user_id: int):
        logger.info(f"Getting User Gym Registration With Id ---> {user_id}")

        user_gym_registration_all = (
            self.db.query(UserGymRegistration)
            .filter(UserGymRegistration.user_id == user_id)
            .filter(UserGymRegistration.is_expired == False)
            .first()
        )

        return user_gym_registration_all

    def create_user_gym_registration(self, user_gym_registration: UserGymRegistration):
        self.db.add(user_gym_registration)
        self.db.commit()
        self.db.refresh(user_gym_registration)
        logger.info(f"[+] User Gym Registration Created With Id ---> {user_gym_registration.id}")
        return user_gym_registration

    def get_user_gym_registration_info(self, user_id: int):
        logger.info(f"Getting User Gym Registration Info With Id ---> {user_id}")

        user_gym_registration_info = (
            self.db.query(UserGymRegistration)
            .filter(UserGymRegistration.user_id == user_id)
            .filter(UserGymRegistration.is_expired == False)
            .first()
        )

        return user_gym_registration_info

    def create_user_gym_comment(self, user_gym_comment: GymComment):
        self.db.add(user_gym_comment)
        self.db.commit()
        self.db.refresh(user_gym_comment)
        logger.info(f"[+] User Gym Comment Created With Id ---> {user_gym_comment.id}")
        return user_gym_comment

    # ************************************************************************
    def user_get_verified_coach_comments(self, coach_id: int):
        logger.info(f"[+] Fetching Verified Coach Comments With Caoch Id ---> {coach_id}")

        verified_gym_comments = (
            self.db.query(CoachComment)
            .filter(CoachComment.coach_id == coach_id)
            .join(Coach, CoachComment.coach_id == Coach.id)
            .filter(Coach.verification_status == "verified")
            .all()
        )

        return verified_gym_comments

    def create_user_coach_comment(self, user_coach_comment: CoachComment):
        self.db.add(user_coach_comment)
        self.db.commit()
        self.db.refresh(user_coach_comment)
        logger.info(f"[+] User Coach Comment Created With Id ---> {user_coach_comment.id}")
        return user_coach_comment

    def user_get_verified_coach_detail(self, coach_id: int):
        logger.info(f"[+] Fetching Verified Coach Detail With Coach Id ---> {coach_id}")

        verified_coach_detail = (
            self.db.query(Coach)
            .filter(Coach.verification_status == "verified")
            .filter(Coach.id == coach_id)
            .first()
        )

        return verified_coach_detail

    def user_get_coach_plan_price(self, coach_id: int):
        logger.info(f"[+] Fetching Coach Plan Price Associated With Coach ---> {coach_id}")

        coach_plan_price = (
            self.db.query(CoachPlanPrice)
            .filter(CoachPlanPrice.coach_id == coach_id)
            .first()
        )

        return coach_plan_price

    def update_coach_rating(self, coach_id: int):
        avg_rating = self.db.query(func.avg(CoachComment.rating)) \
            .filter(CoachComment.coach_id == coach_id).scalar()

        if avg_rating is None:
            avg_rating = 0

        coach_metrics = self.db.query(CoachMetrics).filter(CoachMetrics.coach_id == coach_id).first()
        if coach_metrics:
            coach_metrics.rating = round(avg_rating)
            self.db.commit()

        logger.info(f"[+] Coach {coach_id} rating updated to {round(avg_rating)}")

    def update_gym_rating(self, gym_id: int):
        avg_rating = self.db.query(func.avg(GymComment.rating)) \
            .filter(GymComment.gym_id == gym_id).scalar()

        if avg_rating is None:
            avg_rating = 0

        gym = self.db.query(Gym).filter(Gym.id == gym_id).first()
        if gym:
            gym.rating = round(avg_rating)
            self.db.commit()

        logger.info(f"[+] Gym {gym_id} rating updated to {round(avg_rating)}")
