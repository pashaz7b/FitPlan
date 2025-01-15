from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends

from app.domain.models.fitplan_model import Admin
from app.domain.schemas.admin_schema import (GetAdminInfoSchema,
                                             SetAdminInfoSchema)
from app.infrastructure.repositories.admin_repository import AdminRepository
from app.subservices.auth.hash_subservice import HashService
from app.subservices.baseconfig import BaseService


class AdminSubService(BaseService):
    def __init__(self,
                 admin_repo: Annotated[AdminRepository, Depends()],
                 hash_subservice: Annotated[HashService, Depends()]
                 ) -> None:
        super().__init__()
        self.admin_repo = admin_repo
        self.hash_subservice = hash_subservice

    # async def create_admin(self, admin_struct: AdminRegisterSchema) -> Admin:
    #     logger.info(f"[+] Creating Admin With Email ---> {admin_struct.email}")
    #     new_admin = Admin(
    #         password=self.hash_subservice.hash_password(admin_struct.password),
    #         user_name=admin_struct.user_name,
    #         name=admin_struct.name,
    #         email=admin_struct.email,
    #         phone_number=admin_struct.phone_number,
    #         gender=admin_struct.gender,
    #         date_of_birth=admin_struct.date_of_birth,
    #     )
    #
    #     created_admin = self.admin_repo.create_admin(new_admin)
    #     return created_admin

    async def update_admin(self, admin_id: int, update_fields: Dict) -> Admin:
        logger.info(f"Updating admin with id {admin_id}")
        return self.admin_repo.update_admin(admin_id, update_fields)

    async def update_admin_by_email(self, email: str, update_fields: Dict) -> Admin:
        logger.info(f"Updating Admin With Email ---> {email}")
        return self.admin_repo.update_admin_by_email(email, update_fields)

    async def delete_admin(self, admin: Admin) -> None:
        logger.info(f"Deleting admin with id {admin.id}")
        return self.admin_repo.delete_admin(admin)

    async def get_admin(self, admin_id: int) -> Admin:
        logger.info(f"Fetching admin with id {admin_id}")
        return self.admin_repo.get_admin(admin_id)

    async def get_admin_by_email(self, email: str) -> Admin:
        logger.info(f"[+] Fetching admin with Email ---> {email}")
        return self.admin_repo.get_admin_by_email(email)

    async def change_admin_info(self, admin_id: int, changes: Dict):
        logger.info(f"Updating admin with id {admin_id} with changes: {changes}")

        admin_changes = {}

        for key, value in changes.items():
            if key in {"password", "user_name", "name", "email", "phone_number", "gender", "date_of_birth"}:
                admin_changes[key] = value

        if admin_changes:
            logger.info(f"Applying user updates: {admin_changes}")
            self.admin_repo.update_admin(admin_id, admin_changes)

        logger.info(f"Admin with id {admin_id} updated successfully")

    async def get_admin_all_users(self, admin_id: int):
        logger.info(f"[+] Fetching All Users Of fitplan for admin With Id ---> {admin_id}")
        return self.admin_repo.get_admin_all_users(admin_id)

    async def get_admin_all_coach(self, admin_id: int):
        logger.info(f"[+] Fetching All Coaches Of fitplan for admin With Id ---> {admin_id}")
        return self.admin_repo.get_admin_all_coach(admin_id)

    async def get_users_for_coach(self, coach_id: int):
        logger.info(f"[+] Fetching All Users Of fitplan for coach With Id ---> {coach_id}")
        return self.admin_repo.get_users_for_coach(coach_id)

    async def get_all_transaction(self, admin_id: int):
        logger.info(f"[+] Fetching All Transactions Of fitplan for admin With Id ---> {admin_id}")
        return self.admin_repo.get_all_transaction(admin_id)
