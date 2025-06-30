from typing import Annotated
from fastapi import APIRouter, status
# from loguru import logger
import httpx

from app.domain.schemas.token_schema import TokenDataSchema
from app.mainservices.coach_auth_service import get_current_coach
from app.domain.schemas.coach_schema import (CoachCreateChatSchema,
                                             CoachCreateChatResponseSchema)

from app.mainservices.coach_mainservice import CoachMainService
from fastapi import WebSocket, Depends

coach_chat_router = APIRouter()


@coach_chat_router.websocket("/ws/chat/{user_id}")
async def coach_chat_websocket_endpoint(
        websocket: WebSocket,
        user_id: int,
        coach_service: CoachMainService = Depends()
):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://iam.localhost/api/v1/coach/panel",
                headers={"Authorization": f"Bearer {token}"}
            )
        response.raise_for_status()
        coach_data = response.json()
        coach_id = int(coach_data["id"])
    except Exception as e:
        await websocket.close(code=1008)
        return

    await coach_service.coach_chat_websocket(websocket, coach_id, int(user_id))


@coach_chat_router.get("/chat/messages/{user_id}", status_code=status.HTTP_200_OK,
                       response_model=list[CoachCreateChatResponseSchema])
async def get_user_messages(
        current_coach: Annotated[TokenDataSchema, Depends(get_current_coach)],
        coach_service: Annotated[CoachMainService, Depends()],
        user_id: int,
        limit: int = 50,
        offset: int = 0
):
    return await coach_service.get_coach_chat_history(user_id, current_coach.id, limit, offset)
