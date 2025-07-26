from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.postgres_db.postgres_database import get_db
from app.domain.models.fitplan_model import (Admin, User,
                                             Coach, Gym,
                                             CoachMetrics,
                                             Present,
                                             WorkoutPlan,
                                             Take,
                                             User, UserTransactionLog, TransactionLog)


class AdminRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def create_admin(self, admin: Admin) -> Admin:
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        logger.info(f"[+] Admin Created With Id ---> {admin.id} And Email ---> {admin.email}")
        return admin

    def update_admin(self, admin_id: int, updated_admin: Dict):
        admin_query = self.db.query(Admin).filter(Admin.id == admin_id)
        db_admin = admin_query.first()
        admin_query.filter(Admin.id == admin_id).update(
            updated_admin, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_admin)
        logger.info(f"[+] Admin With Id ---> {admin_id} Updated")
        return db_admin

    def update_admin_by_email(self, admin_email: str, updated_admin: Dict):
        admin_query = self.db.query(Admin).filter(Admin.email == admin_email)
        db_admin = admin_query.first()
        admin_query.filter(Admin.email == admin_email).update(
            updated_admin, synchronize_session=False
        )
        self.db.commit()
        self.db.refresh(db_admin)
        logger.info(f"[+] Admin With Email ---> {admin_email} Updated")
        return db_admin

    def delete_admin(self, admin: Admin) -> None:
        self.db.delete(admin)
        self.db.commit()
        self.db.flush()
        logger.info(f"[+] Admin Deleted With Id ---> {admin.id} And Email ---> {admin.email}")

    def get_admin(self, admin_id: int):
        logger.info(f"[+] Fetching Admin With Id ---> {admin_id}")
        return self.db.query(Admin).filter(Admin.id == admin_id).first()

    def get_admin_by_email(self, email: str):
        logger.info(f"[+] Fetching Admin With Email --> {email}")
        return self.db.query(Admin).filter(Admin.email == email).first()

    def get_admin_all_users(self, admin_id: int):
        logger.info(f"[+] Fetching All Users Of fitplan for admin With Id ---> {admin_id}")

        all_users = (
            self.db.query(User)
            .join(Take, User.id == Take.user_id)
            .join(WorkoutPlan, WorkoutPlan.id == Take.workout_plan_id)
            .join(Present, Present.workout_plan_id == WorkoutPlan.id)
            .join(Coach, Coach.id == Present.coach_id)
            .all()
        )

        return all_users

    def get_admin_all_coach(self, admin_id: int):
        logger.info(f"[+] Fetching All Coach Of fitplan for admin With Id ---> {admin_id}")

        all_coach = (
            self.db.query(Coach)
            .join(Present, Present.coach_id == Coach.id)
            .join(WorkoutPlan, WorkoutPlan.id == Present.workout_plan_id)
            .join(Take, Take.workout_plan_id == WorkoutPlan.id)
            .join(User, User.id == Take.user_id)
            .all()
        )

        return all_coach

    def get_users_for_coach(self, coach_id: int):
        logger.info(f"[+] Fetching All Users Of FitPlan for coach With Id ---> {coach_id}")

        all_users = (
            self.db.query(User)
            .join(Take, User.id == Take.user_id)
            .join(WorkoutPlan, WorkoutPlan.id == Take.workout_plan_id)
            .join(Present, Present.workout_plan_id == WorkoutPlan.id)
            .join(Coach, Coach.id == Present.coach_id)
            .filter(Coach.id == coach_id)
            .all()
        )

        return all_users

    def get_all_transaction(self, admin_id: int):
        logger.info(f"[+] Fetching All Transaction Of FitPlan for admin With Id ---> {admin_id}")

        all_transaction = (
            self.db.query(User)
            .join(UserTransactionLog, User.id == UserTransactionLog.user_id)
            .join(TransactionLog, TransactionLog.id == UserTransactionLog.transaction_id)
            .all()
        )

        return all_transaction

    # ********************************************************
    def admin_get_coach_to_verify(self, admin_id: int):
        logger.info(f"[+] Fetching All Coach To Verify By Admin With Id ---> {admin_id}")
        coach_to_verify = (
            self.db.query(Coach)
            .filter(Coach.is_verified == True)
            .filter(Coach.verification_status == "pending")
            .all()
        )
        return coach_to_verify

    def admin_update_coach_verification(self, coach_id: int, verification_status: str):
        logger.info(f"[+] Updating Coach Verification Status For Coach With Id ---> {coach_id}")
        coach_query = self.db.query(Coach).filter(Coach.id == coach_id)
        db_coach = coach_query.first()
        coach_query.update({"verification_status": verification_status}, synchronize_session=False)
        self.db.commit()
        self.db.refresh(db_coach)
        logger.info(f"[+] Coach Verification Status Updated For Coach With Id ---> {coach_id}")
        return db_coach

    def check_gym_exits(self, gym_id: int):
        logger.info(f"[+] Checking If Gym Exists With Id ---> {gym_id}")
        gym = (self.db.query(Gym)
               .filter(Gym.id == gym_id)
               .first()
        )
        return gym

    def admin_get_gym_to_verify(self, admin_id: int):
        logger.info(f"[+] Fetching All Gym To Verify By Admin With Id ---> {admin_id}")
        gym_to_verify = (
            self.db.query(Gym)
            .filter(Gym.verification_status == "pending")
            .all()
        )
        return gym_to_verify

    def admin_update_gym_verification(self, gym_id: int, verification_status: str):
        logger.info(f"[+] Updating Gym Verification Status For Gym With Id ---> {gym_id}")
        gym_query = self.db.query(Gym).filter(Gym.id == gym_id)
        db_gym = gym_query.first()
        gym_query.update({"verification_status": verification_status}, synchronize_session=False)
        self.db.commit()
        self.db.refresh(db_gym)
        logger.info(f"[+] Gym Verification Status Updated For Gym With Id ---> {gym_id}")
        return db_gym