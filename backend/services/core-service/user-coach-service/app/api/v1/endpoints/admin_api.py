from typing import Annotated
from fastapi import APIRouter, Depends, status
from loguru import logger

from app.domain.schemas.token_schema import TokenDataSchema
from app.mainservices.admin_auth_service import get_current_admin
from app.domain.schemas.admin_schema import (GetAdminInfoSchema,
                                             SetAdminInfoSchema, GetAdminAllUsersSchema)

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


@admin_core_router.put(
    "/change_admin_info",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def change_admin_info(
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        admin_data: SetAdminInfoSchema,
        admin_service: Annotated[AdminMainService, Depends()]
):
    logger.info(f'Change Admin info for Admin {current_admin.id}')
    return await admin_service.change_admin_info(current_admin.id, admin_data)


@admin_core_router.get(
    "/get_all_users",
    response_model=list[GetAdminAllUsersSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_users(
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        admin_service: Annotated[AdminMainService, Depends()]
):
    logger.info(f'Get all users for admin {current_admin.id}')
    return await admin_service.get_admin_all_users(current_admin.id)
