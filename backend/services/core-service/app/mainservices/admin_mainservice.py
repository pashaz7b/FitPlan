from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status

from app.domain.schemas.admin_schema import (GetAdminInfoSchema,
                                             SetAdminInfoSchema, GetAdminAllUsersSchema, GetAdminAllCoachSchema,
                                             UserSchema, TransactionSchema, GetAdminAllTransactionSchema,
                                             AdminGetCoachToVerifySchema, AdminUpdateCoachVerificationSchema,
                                             AdminGetGymToVerifySchema, AdminUpdateGymVerificationSchema)

from app.subservices.admin_subservice import AdminSubService
from app.subservices.coach_subservice import CoachSubService
from app.subservices.user_subservice import UserSubService
from app.subservices.user_duplicates_subservice import UserDuplicatesSubService
from app.subservices.baseconfig import BaseService
from app.subservices.auth.hash_subservice import HashService


class AdminMainService(BaseService):
    def __init__(self,
                 admin_subservice: Annotated[AdminSubService, Depends()],
                 coach_subservice: Annotated[CoachSubService, Depends()],
                 user_subservice: Annotated[UserSubService, Depends()],
                 user_duplicates_subservice: Annotated[UserDuplicatesSubService, Depends()],
                 hash_subservice: Annotated[HashService, Depends()]
                 ) -> None:
        super().__init__()
        self.admin_subservice = admin_subservice
        self.coach_subservice = coach_subservice
        self.uer_subservice = user_subservice
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

    async def get_admin_info(self, admin_id: int) -> GetAdminInfoSchema:
        admin = await self.admin_subservice.get_admin(admin_id)

        empty_password = ""
        return GetAdminInfoSchema(
            password=empty_password,
            user_name=admin.user_name,
            name=admin.name,
            email=admin.email,
            phone_number=admin.phone_number,
            gender=admin.gender,
            date_of_birth=admin.date_of_birth,
        )

    async def change_admin_info(self, admin_id: int, admin: SetAdminInfoSchema):
        current_admin = await self.admin_subservice.get_admin(admin_id)

        current_data = {
            "password": current_admin.password,
            "user_name": current_admin.user_name,
            "name": current_admin.name,
            "email": current_admin.email,
            "phone_number": current_admin.phone_number,
            "gender": current_admin.gender,
            "date_of_birth": current_admin.date_of_birth,
        }

        if admin.password.strip():
            admin.password = self.hash_subservice.hash_password(admin.password) if admin.password else None

        changes = {key: value for key, value in admin if current_data.get(key) != value}

        if not admin.password.strip():
            changes.pop("password")

        if "email" in changes:
            await self.check_email_existence(admin.email)

        if "phone_number" in changes:
            await self.check_phone_number_existence(admin.phone_number)

        if "user_name" in changes:
            await self.check_user_name_existence(admin.user_name)

        if changes:
            await self.admin_subservice.change_admin_info(admin_id, changes)

        return {"message": "Admin information updated successfully" if changes else "No changes detected"}

    async def get_admin_all_users(self, admin_id: int):
        logger.info(f"[+] Fetching All Users Of fitplan for admin With Id ---> {admin_id}")

        users = await self.admin_subservice.get_admin_all_users(admin_id)

        if not users:
            logger.error(f"[-] No User Found In Fitplan")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No User Found In Fitplan"
            )

        result = []
        empty_password = ""

        # for user in users:
        #     coach = None
        #     for take in user.takes:
        #         workout_plan = take.workout_plan
        #         if workout_plan and workout_plan.present:
        #             coach = workout_plan.present[0].coach  # فرض بر این است که یک مربی مرتبط وجود دارد
        #             break  # اگر فقط به اولین مربی نیاز دارید، حلقه را متوقف کنید
        #
        #     result.append(GetAdminAllUsersSchema(
        #         user_id=user.id,
        #         user_password=empty_password,
        #         user_user_name=user.user_name,
        #         user_name=user.name,
        #         user_email=user.email,
        #         user_phone_number=user.phone_number,
        #         user_gender=user.gender,
        #         user_date_of_birth=user.date_of_birth,
        #         user_height=user.metrics.height if user.metrics else None,
        #         user_weight=user.metrics.weight if user.metrics else None,
        #         coach_id=coach.id if coach else None,
        #         coach_password=empty_password,
        #         coach_user_name=coach.user_name if coach else None,
        #         coach_name=coach.name if coach else None,
        #         coach_email=coach.email if coach else None,
        #         coach_phone_number=coach.phone_number if coach else None,
        #         coach_gender=coach.gender if coach else None,
        #         coach_status=coach.status if coach else None,
        #         coach_date_of_birth=coach.date_of_birth if coach else None,
        #         coach_height=coach.metrics.height if coach and coach.metrics else None,
        #         coach_weight=coach.metrics.weight if coach and coach.metrics else None,
        #         coach_specialization=coach.metrics.specialization if coach else None,
        #         coach_biography=coach.metrics.biography if coach else None
        #     ))

        for user in users:
            coach = None
            last_take = user.takes[-1] if user.takes else None

            if last_take:
                workout_plan = last_take.workout_plan
                if workout_plan and workout_plan.present:
                    coach = workout_plan.present[0].coach

            result.append(GetAdminAllUsersSchema(
                user_id=user.id,
                user_password=empty_password,
                user_user_name=user.user_name,
                user_name=user.name,
                user_email=user.email,
                user_phone_number=user.phone_number,
                user_gender=user.gender,
                user_date_of_birth=user.date_of_birth,
                user_height=user.metrics.height if user.metrics else None,
                user_weight=user.metrics.weight if user.metrics else None,
                coach_id=coach.id if coach else None,
                coach_password=empty_password,
                coach_user_name=coach.user_name if coach else None,
                coach_name=coach.name if coach else None,
                coach_email=coach.email if coach else None,
                coach_phone_number=coach.phone_number if coach else None,
                coach_gender=coach.gender if coach else None,
                coach_status=coach.status if coach else None,
                coach_date_of_birth=coach.date_of_birth if coach else None,
                coach_height=coach.metrics.height if coach and coach.metrics else None,
                coach_weight=coach.metrics.weight if coach and coach.metrics else None,
                coach_specialization=coach.metrics.specialization if coach else None,
                coach_biography=coach.metrics.biography if coach else None
            ))

        return result

    async def get_admin_all_coach(self, admin_id: int):
        logger.info(f"[+] Fetching All Coach Of fitplan for admin With Id ---> {admin_id}")

        coaches = await self.admin_subservice.get_admin_all_coach(admin_id)

        if not coaches:
            logger.error(f"[-] No Coach Found In Fitplan")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No Coach Found In Fitplan"
            )

        result = []
        empty_password = ""

        for coach in coaches:
            users = await self.admin_subservice.get_users_for_coach(coach.id)

            coach_data = GetAdminAllCoachSchema(
                coach_id=coach.id,
                coach_password=empty_password,
                coach_user_name=coach.user_name,
                coach_name=coach.name,
                coach_email=coach.email,
                coach_phone_number=coach.phone_number,
                coach_gender=coach.gender,
                coach_status=coach.status,
                coach_date_of_birth=coach.date_of_birth,
                coach_height=coach.metrics.height if coach.metrics else None,
                coach_weight=coach.metrics.weight if coach.metrics else None,
                coach_specialization=coach.metrics.specialization if coach.metrics else None,
                coach_biography=coach.metrics.biography if coach.metrics else None,
                users=[
                    UserSchema(
                        user_id=user.id,
                        user_password=empty_password,
                        user_user_name=user.user_name,
                        user_name=user.name,
                        user_email=user.email,
                        user_phone_number=user.phone_number,
                        user_gender=user.gender,
                        user_date_of_birth=user.date_of_birth,
                        user_height=user.metrics.height if user.metrics else None,
                        user_weight=user.metrics.weight if user.metrics else None,
                    )
                    for user in users
                ],
            )

            result.append(coach_data)

        logger.info(f"[+] Successfully fetched {len(result)} coaches and their users")
        return result

    async def get_all_transaction(self, admin_id: int):
        logger.info(f"[+] Fetching All Transactions Of fitplan for admin With Id ---> {admin_id}")

        users_transactions = await self.admin_subservice.get_all_transaction(admin_id)

        if not users_transactions:
            logger.error(f"[-] No Transaction Found In Fitplan")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No Transaction Found In Fitplan"
            )

        result = []
        empty_password = ""

        for user in users_transactions:
            transactions = [
                TransactionSchema(
                    transaction_id=transaction_log.transaction.id,
                    transaction_amount=transaction_log.transaction.amount,
                    transaction_reason=transaction_log.transaction.reason,
                    transaction_status=transaction_log.transaction.status,
                    transaction_date=transaction_log.transaction.date,
                    created_at=transaction_log.transaction.created_at,
                    updated_at=transaction_log.transaction.updated_at,
                )
                for transaction_log in user.user_transactions
            ]

            user_data = GetAdminAllTransactionSchema(
                user_id=user.id,
                user_password=empty_password,
                user_user_name=user.user_name,
                user_name=user.name,
                user_email=user.email,
                user_phone_number=user.phone_number,
                user_gender=user.gender,
                user_date_of_birth=user.date_of_birth,
                user_height=user.metrics.height if user.metrics else None,
                user_weight=user.metrics.weight if user.metrics else None,
                transactions=transactions,
            )

            result.append(user_data)

        logger.info(f"[+] Successfully fetched {len(result)} users and their transactions")
        return result

    async def check_coach_exits(self, coach_id: int):
        coach = await self.coach_subservice.get_coach(coach_id)
        if not coach:
            logger.error(f"[-] Coach With Id ---> {coach_id} Not Found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Coach Not Found"
            )
        return coach

    async def check_user_exits(self, user_id: int):
        user = await self.uer_subservice.get_user(user_id)
        if not user:
            logger.error(f"[-] User With Id ---> {user_id} Not Found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
            )
        return user

    async def admin_get_coach_to_verify(self, admin_id: int):
        logger.info(f"[+] Fetching All Coaches To Verify for admin With Id ---> {admin_id}")

        coaches = await self.admin_subservice.admin_get_coach_to_verify(admin_id)

        if not coaches:
            logger.error(f"[-] No Coach Found In Fitplan")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No Coach Found In Fitplan"
            )

        result = []

        for coach in coaches:
            metrics = coach.metrics

            result.append(AdminGetCoachToVerifySchema(
                coach_id=coach.id,
                coaching_id=metrics.coaching_id if metrics else None,
                coach_user_name=coach.user_name,
                coach_name=coach.name,
                coach_email=coach.email,
                coach_phone_number=coach.phone_number,
                coach_gender=coach.gender,
                coach_status=coach.status,
                coach_date_of_birth=coach.date_of_birth,
                coach_height=metrics.height if metrics else None,
                coach_weight=metrics.weight if metrics else None,
                coach_specialization=metrics.specialization if metrics else None,
                coach_biography=metrics.biography if metrics else None,
            ))

        return result

    async def admin_update_coach_verification(self, coach_verification_schema: AdminUpdateCoachVerificationSchema):
        coach_id = coach_verification_schema.coach_id
        coach_verification_status = coach_verification_schema.verification_status
        coach = await self.coach_subservice.get_coach(coach_id)
        if not coach:
            logger.error(f"[-] Coach With Id ---> {coach_id} Not Found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Coach Not Found"
            )

        verification_status = "verified" if coach_verification_status else "rejected"
        logger.info(f"[+] Updating Coach Status for Coach With Id ---> {coach_id} to {verification_status}")
        return await self.admin_subservice.admin_update_coach_verification(coach_id, verification_status)

    async def admin_get_gym_to_verify(self, admin_id: int):
        logger.info(f"[+] Fetching All Gyms To Verify by admin With Id ---> {admin_id}")
        gyms = await self.admin_subservice.admin_get_gym_to_verify(admin_id)

        if not gyms:
            logger.error(f"[-] No Gym Found In FitPlan")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No Gym Found In FitPlan"
            )

        result = []

        for gym in gyms:
            result.append(AdminGetGymToVerifySchema(
                gym_id=gym.id,
                gym_owner_id=gym.owner_id,
                gym_name=gym.name,
                gym_license_number=gym.license_number,
                gym_location=gym.location,
                gym_sport_facilities=gym.sport_facilities,
                gym_welfare_facilities=gym.welfare_facilities,
                gym_rating=gym.rating
            ))

        return result

    async def admin_update_gym_verification(self, gym_verification_schema: AdminUpdateGymVerificationSchema):
        gym_id = gym_verification_schema.gym_id
        gym_verification_status = gym_verification_schema.verification_status
        gym = await self.admin_subservice.check_gym_exits(gym_id)
        if not gym:
            logger.error(f"[-] Gym With Id ---> {gym_id} Not Found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Gym Not Found"
            )

        verification_status = "verified" if gym_verification_status else "rejected"
        logger.info(f"[+] Updating Gym Status for Gym With Id ---> {gym_id} to {verification_status}")
        return await self.admin_subservice.admin_update_gym_verification(gym_id, verification_status)