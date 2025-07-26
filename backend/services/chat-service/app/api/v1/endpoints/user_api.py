from typing import Annotated
from fastapi import APIRouter, Depends, status
from loguru import logger
import httpx

from app.domain.schemas.token_schema import TokenDataSchema
from app.mainservices.user_auth_service import get_current_user
from app.domain.schemas.user_schema import (UserCreateChatSchema,
                                            UserCreateChatResponseSchema)

from app.mainservices.user_mainservice import UserMainService
from fastapi import FastAPI, WebSocket, Depends
from app.core.config.config import get_settings
user_chat_router = APIRouter()


@user_chat_router.websocket("/ws/chat")
async def user_chat_websocket_endpoint(
        websocket: WebSocket,
        user_service: UserMainService = Depends()
):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    try:
        async with httpx.AsyncClient() as client:
            iam_url = get_settings().IAM_URL
            response = await client.get(
                f"{iam_url}/api/v1/users/panel",
                headers={"Authorization": f"Bearer {token}"}
            )
        response.raise_for_status()
        user_data = response.json()
        user_id = int(user_data["id"])
    except Exception as e:
        await websocket.close(code=1008)
        return

    await user_service.user_chat_websocket(websocket, user_id)


@user_chat_router.get("/chat/messages", status_code=status.HTTP_200_OK,
                      response_model=list[UserCreateChatResponseSchema])
async def get_user_messages(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_service: Annotated[UserMainService, Depends()],
        limit: int = 50,
        offset: int = 0
):
    return await user_service.get_user_chat_history(current_user.id, limit, offset)
