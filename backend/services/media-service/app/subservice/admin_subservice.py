from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends

from app.domain.models.admin_model import Admin
from app.infrastructure.repositories.admin_repository import AdminRepository


class AdminSubService():
    def __init__(self,
                 admin_repo: Annotated[AdminRepository, Depends()],
                 ) -> None:
        self.admin_repo = admin_repo

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
