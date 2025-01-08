from typing import Annotated
from loguru import logger
from fastapi import Depends
from app.core.config.config import get_settings, Settings
from app.domain.schemas.token_schema import TokenDataSchema
from app.infrastructure.clients.http_client import HTTPClient


class IAMClient:
    def __init__(
            self,
            http_client: Annotated[HTTPClient, Depends()],
            config: Settings = Depends(get_settings),
    ):
        self.config = config
        self.http_client = http_client

    async def validate_token(self, token: str) -> TokenDataSchema:
        headers = {"Authorization": f"Bearer {token}"}
        async with self.http_client as client:
            response = await client.get(
                f"{self.config.IAM_URL}/api/v1/users/panel", headers=headers
            )
            response.raise_for_status()
            logger.info(f"Token {token} validated")
            return TokenDataSchema(**response.json())

    async def validate_coach_token(self, token: str) -> TokenDataSchema:
        headers = {"Authorization": f"Bearer {token}"}
        async with self.http_client as client:
            response = await client.get(
                f"{self.config.IAM_URL}/api/v1/coach/panel", headers=headers
            )
            response.raise_for_status()
            logger.info(f"Token {token} validated")
            return TokenDataSchema(**response.json())
