from typing import Annotated
from fastapi import APIRouter, Depends, status
from loguru import logger

from app.domain.schemas.token_schema import TokenDataSchema
from app.mainservices.admin_auth_service import get_current_admin
from app.domain.schemas.admin_schema import (GetAdminInfoSchema,
                                             SetAdminInfoSchema)

from app.mainservices.admin_mainservice import AdminMainService

admin_core_router = APIRouter()


@admin_core_router.get(
    "/get_admin_info",
    response_model=GetAdminInfoSchema,
    status_code=status.HTTP_200_OK
)
async def get_admin_info(
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        admin_service: Annotated[AdminMainService, Depends()]
):
    logger.info(f'Get admin info for admin {current_admin.id}')
    return await admin_service.get_admin_info(current_admin.id)
