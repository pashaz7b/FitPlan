from datetime import datetime, timedelta, timezone
from typing import Annotated
from loguru import logger
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.domain.models.admin_model import Admin
from app.domain.schemas.token_schema import TokenSchema
from app.domain.schemas.admin_schema import AdminLoginSchema
from app.subservices.auth.hash_subservice import HashService
from app.subservices.baseconfig import BaseService
from app.subservices.admin_subservice import AdminSubService
from app.validators.regex_checker import RegexChecker

admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/admin/login")

class AuthService(BaseService):
    def __init__(
            self,
            hash_service: Annotated[HashService, Depends()],
            admin_service: Annotated[AdminSubService, Depends()],
    ) -> None:
        super().__init__()
        self.admin_service = admin_service
        self.hash_service = hash_service

    async def authenticate_admin(self, admin: AdminLoginSchema) -> TokenSchema:

        email_regex_check = RegexChecker.is_valid_email(admin.email)

        if not email_regex_check:
            logger.error(f"[-] Invalid Email ---> {admin.email} format")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Email Format"
            )

        existing_admin = await self.admin_service.get_admin_by_email(
            admin.email
        )
        logger.info(f"[...] Authenticating Admin With Email ---> {admin.email}")

        if not existing_admin:
            logger.error(f"[-] Admin With Email ---> {admin.email} Does Not Exist")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Admin Does Not Exist"
            )

        if not existing_admin.is_verified:
            logger.error(f"[-] Admin with Email {admin.email} Is Not Verified")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Admin Is Not Verified"
            )

        if not self.hash_service.verify_password(
                admin.password, existing_admin.password
        ):
            logger.error(f"[-] Invalid Password For Admin With Email ---> {admin.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self.create_access_token(data={"sub": str(existing_admin.id)})

        logger.info(f"[+] Admin With Email ---> {admin.email} Authenticated Successfully")
        return TokenSchema(access_token=access_token, token_type="bearer")

    def create_access_token(self, data: dict) -> str:
        logger.info("[...] Creating Access Token")
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            self.config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.config.JWT_SECRET_KEY, algorithm=self.config.JWT_ALGORITHM
        )
        return encoded_jwt


async def get_current_admin(
        token: Annotated[str, Depends(admin_oauth2_scheme)],
        admin_service: Annotated[AdminSubService, Depends()],
) -> Admin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could Not Validate Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logger.info(f"[...] Validating Token {token}")
    try:
        payload = jwt.decode(
            token,
            admin_service.config.JWT_SECRET_KEY,
            algorithms=[admin_service.config.JWT_ALGORITHM],
        )
        admin_id: int = payload.get("sub")
        admin = await admin_service.get_admin(admin_id)
        if admin_id is None:
            logger.error("[-] Could Not Validate Credentials")
            raise credentials_exception
    except jwt.PyJWTError:
        logger.error("[-] Error Decoding Token")
        raise credentials_exception

    logger.info(f"[+] Admin With Id ---> {admin_id} Validated Successfully")
    return admin
