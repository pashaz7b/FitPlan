from typing import Annotated, Dict
from loguru import logger
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.postgres.postgres_database import get_db
from app.domain.models.admin_model import Admin


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
