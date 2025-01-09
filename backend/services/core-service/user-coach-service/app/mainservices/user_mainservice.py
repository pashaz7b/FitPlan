from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status

from app.domain.schemas.user_schema import GetUserInfoSchema, SetUserInfoSchema, GetUserTransactionsSchema

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
        return GetUserInfoSchema(
            id=user.id,
            password=user.password,
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

        user.password = self.hash_subservice.hash_password(user.password) if user.password else None

        changes = {key: value for key, value in user if current_data.get(key) != value}

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
            logger.info(f"[+] No transactions found for user with id ---> {user_id}")
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
