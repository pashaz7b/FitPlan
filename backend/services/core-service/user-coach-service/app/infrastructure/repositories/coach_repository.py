from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.postgres_db.postgres_database import get_db
from app.domain.models.fitplan_model import (Coach,
                                             CoachMetrics,
                                             Present,
                                             WorkoutPlan,
                                             Take,
                                             User, UserRequestMeal, UserMeal,
                                             UserMealMealSupplement)


class CoachRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def create_coach(self, coach: Coach) -> Coach:
        self.db.add(coach)
        self.db.commit()
        self.db.refresh(coach)
        logger.info(f"[+] Coach Created With Id ---> {coach.id} And Email ---> {coach.email}")
        return coach

    def create_coach_metrics(self, metrics: CoachMetrics) -> CoachMetrics:
        self.db.add(metrics)
        self.db.commit()
        self.db.refresh(metrics)
        logger.info(f"[+] Metrics Created For Coach Id ---> {metrics.coach_id}")
        return metrics

    def update_coach(self, coach_id: int, updated_coach: Dict):
        coach_query = self.db.query(Coach).filter(Coach.id == coach_id)
        db_coach = coach_query.first()
        coach_query.filter(Coach.id == coach_id).update(
            updated_coach, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_coach)
        logger.info(f"[+] Coach With Id ---> {coach_id} Updated")
        return db_coach

    def update_coach_metrics(self, coach_id: int, updated_metrics: Dict):
        metrics_query = self.db.query(CoachMetrics).filter(CoachMetrics.coach_id == coach_id)
        db_metrics = metrics_query.first()
        if not db_metrics:
            logger.warning(f"[-] Metrics For Coach Id ---> {coach_id} Not Found")
            return None
        metrics_query.update(updated_metrics, synchronize_session=False)
        self.db.commit()
        self.db.refresh(db_metrics)
        logger.info(f"[+] Metrics For Coach Id ---> {coach_id} Updated")
        return db_metrics

    def update_coach_by_email(self, coach_email: str, updated_coach: Dict):
        coach_query = self.db.query(Coach).filter(Coach.email == coach_email)
        db_coach = coach_query.first()
        coach_query.filter(Coach.email == coach_email).update(
            updated_coach, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_coach)
        logger.info(f"[+] Coach With Email ---> {coach_email} Updated")
        return db_coach

    def delete_coach(self, coach: Coach) -> None:
        self.db.delete(coach)
        self.db.commit()
        self.db.flush()
        logger.info(f"[+] Coach Deleted With Id ---> {coach.id} And Email ---> {coach.email}")

    def get_coach(self, coach_id: int):
        logger.info(f"[+] Fetching Coach With Id ---> {coach_id}")
        return self.db.query(Coach).filter(Coach.id == coach_id).first()

    def get_coach_metrics(self, coach_id: int):
        logger.info(f"[+] Fetching Coach Metrics With Id ---> {coach_id}")
        return self.db.query(CoachMetrics).filter(CoachMetrics.id == coach_id).first()

    def get_coach_by_email(self, email: str):
        logger.info(f"[+] Fetching Coach With Email --> {email}")
        return self.db.query(Coach).filter(Coach.email == email).first()

    def get_coach_user(self, coach_id: int):
        logger.info(f"[+] Fetching Coach With Id ---> {coach_id}")

        my_users = (
            self.db.query(User)
            .join(Take, User.id == Take.user_id)
            .join(WorkoutPlan, WorkoutPlan.id == Take.workout_plan_id)
            .join(Present, Present.workout_plan_id == WorkoutPlan.id)
            .filter(Present.coach_id == coach_id)
            .all()
        )
        return my_users

    def get_coach_user_meal_request(self, coach_id: int):
        logger.info(f"[+] Fetching Coach With Id ---> {coach_id}")

        # my_users = (
        #     self.db.query(User)
        #     .join(UserRequestMeal, User.id == UserRequestMeal.user_id)
        #     .join(UserMeal, UserMeal.id == UserRequestMeal.user_meal_id)
        #     .join(Take, User.id == Take.user_id)
        #     .join(WorkoutPlan, WorkoutPlan.id == Take.workout_plan_id)
        #     .join(Present, Present.workout_plan_id == WorkoutPlan.id)
        #     .filter(Present.coach_id == coach_id)
        #     .all()
        # )
        my_users = (
            self.db.query(User)
            .join(UserRequestMeal, User.id == UserRequestMeal.user_id)
            .join(UserMeal, UserMeal.id == UserRequestMeal.user_meal_id)
            .join(Take, User.id == Take.user_id)
            .join(WorkoutPlan, WorkoutPlan.id == Take.workout_plan_id)
            .join(Present, Present.workout_plan_id == WorkoutPlan.id)
            .outerjoin(UserMealMealSupplement, UserMeal.id == UserMealMealSupplement.user_meal_id)
            .filter(Present.coach_id == coach_id)
            .filter(UserMealMealSupplement.user_meal_id.is_(None))
            .all()
        )
        return my_users

    # def get_coach_user_meal_meal_supplement(self, coach_id: int):
    #     pass
