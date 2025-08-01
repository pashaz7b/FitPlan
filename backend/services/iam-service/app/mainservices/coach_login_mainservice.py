from datetime import datetime, timedelta, timezone
from typing import Annotated
from loguru import logger
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.domain.models.coach_model import Coach
from app.domain.schemas.token_schema import TokenSchema
from app.domain.schemas.coach_schema import CoachLoginSchema
from app.subservices.auth.hash_subservice import HashService
from app.subservices.baseconfig import BaseService
from app.subservices.coach_subservice import CoachSubService
from app.validators.regex_checker import RegexChecker

coach_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/coach/login", scheme_name="CoachOAuth2")


class AuthService(BaseService):
    def __init__(
            self,
            hash_service: Annotated[HashService, Depends()],
            coach_service: Annotated[CoachSubService, Depends()],
    ) -> None:
        super().__init__()
        self.coach_service = coach_service
        self.hash_service = hash_service

    async def authenticate_coach(self, coach: CoachLoginSchema) -> TokenSchema:

        email_regex_check = RegexChecker.is_valid_email(coach.email)

        if not email_regex_check:
            logger.error(f"[-] Invalid Email ---> {coach.email} format")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Email Format"
            )

        existing_coach = await self.coach_service.get_coach_by_email(
            coach.email
        )
        logger.info(f"[...] Authenticating Coach With Email ---> {coach.email}")

        if not existing_coach:
            logger.error(f"[-] Coach With Email ---> {coach.email} Does Not Exist")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Coach Does Not Exist"
            )

        if not existing_coach.is_verified:
            logger.error(f"[-] Coach with Email {coach.email} Is Not Verified")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Coach Is Not Verified"
            )

        if existing_coach.verification_status != "verified":
            logger.error(f"[-] Coach with Email {coach.email} Is Not Verified by admin")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Coach Is Not Verified by admin"
            )

        if not self.hash_service.verify_password(
                coach.password, existing_coach.password
        ):
            logger.error(f"[-] Invalid Password For Coach With Email ---> {coach.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self.create_access_token(data={"sub": str(existing_coach.id)})

        logger.info(f"[+] Coach With Email ---> {coach.email} Authenticated Successfully")
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


async def get_current_coach(
        token: Annotated[str, Depends(coach_oauth2_scheme)],
        coach_service: Annotated[CoachSubService, Depends()],
) -> Coach:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could Not Validate Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logger.info(f"[...] Validating Token {token}")
    try:
        payload = jwt.decode(
            token,
            coach_service.config.JWT_SECRET_KEY,
            algorithms=[coach_service.config.JWT_ALGORITHM],
        )
        coach_id: int = payload.get("sub")
        coach = await coach_service.get_coach(coach_id)
        if coach_id is None:
            logger.error("[-] Could Not Validate Credentials")
            raise credentials_exception
    except jwt.PyJWTError:
        logger.error("[-] Error Decoding Token")
        raise credentials_exception

    logger.info(f"[+] Coach With Id ---> {coach_id} Validated Successfully")
    return coach
