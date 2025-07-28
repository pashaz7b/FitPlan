# import json
# from typing import Annotated

from loguru import logger
# from fastapi import Depends, HTTPException, status
from app.mainservices.singletons import get_coach_connection_manager, get_user_connection_manager
from app.domain.schemas.coach_schema import (CoachCreateChatSchema,
                                             CoachCreateChatResponseSchema)
from app.subservices.coch_subservice import CoachSubService
# from app.subservices.baseconfig import BaseService
from fastapi import WebSocket, Depends
# from json.decoder import JSONDecodeError
from fastapi import WebSocketDisconnect, HTTPException
# from collections import defaultdict
import json
from typing import Annotated


# class CoachConnectionManager:
#     def __init__(self):
#         self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)
#
#     async def connect(self, coach_id: int, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections[coach_id].append(websocket)
#
#     def disconnect(self, coach_id: int, websocket: WebSocket):
#         self.active_connections[coach_id].remove(websocket)
#
#     # async def send_personal_message(self, message, user_id: int, user_connections: dict[int, list[WebSocket]]):
#     #     for websocket in user_connections.get(user_id, []):
#     #         await websocket.send_json(message)
#
#     async def send_message_to_user(self, message, user_id: int):
#         for ws in self.active_connections.get(user_id, []):
#             await ws.send_json(message)


# class CoachMainService:
#     def __init__(self,
#                  coach_subservice: Annotated[CoachSubService, Depends()],
#                  user_connection_manager: Annotated[UserConnectionManager, Depends()],
#                  ):
#         self.coach_subservice = coach_subservice
#         self.manager = CoachConnectionManager()
#         self.user_connection_manager = user_connection_manager
#
#     async def coach_chat_websocket(self, websocket: WebSocket, coach_id: int):
#         await self.manager.connect(coach_id, websocket)
#         try:
#             while True:
#                 data = await websocket.receive_text()
#                 logger.info(f"coach message ----> {data}")
#
#                 if not data.strip():
#                     await websocket.send_json({"error": "empty input"})
#                     continue
#
#                 try:
#                     json_data = json.loads(data)
#                     content = json_data.get("content", "")
#                     user_id = int(json_data.get("user_id"))
#                 except Exception:
#                     await websocket.send_json({"error": "invalid data format"})
#                     continue
#
#                 saved = await self.coach_subservice.create_coach_chat(coach_id, user_id, content)
#
#                 await self.manager.send_message_to_user(
#                     {"content": content, "sender_type": "coach"}, user_id
#                 )
#
#         except WebSocketDisconnect:
#             self.manager.disconnect(coach_id, websocket)
#
#     # async def get_coach_chat_history(self, coach_id: int, user_id: int, limit: int = 50, offset: int = 0):
#     #     messages = await self.coach_subservice.get_coach_chat_messages(coach_id, user_id, limit, offset)
#     #     return [UserCreateChatResponseSchema.from_orm(msg) for msg in messages]

class CoachMainService:
    def __init__(
            self,
            coach_subservice: Annotated[CoachSubService, Depends()],
            # user_connection_manager: Annotated[UserConnectionManager, Depends()],
    ):
        self.coach_subservice = coach_subservice
        self.manager = get_coach_connection_manager()
        self.user_connection_manager = get_user_connection_manager()

    async def coach_chat_websocket(self, websocket: WebSocket, coach_id: int, user_id: int):
        await self.manager.connect(coach_id, websocket)
        try:
            while True:
                data = await websocket.receive_text()
                logger.info(f"Coach message from {coach_id} ----> {data}")

                if not data.strip():
                    await websocket.send_json({"error": "Empty input"})
                    continue

                # try:
                #     json_data = json.loads(data)
                #     chat_data = CoachCreateChatSchema(content=data)
                # except json.JSONDecodeError:
                #     chat_data = CoachCreateChatSchema(content=data)
                #     json_data = chat_data.dict()
                # except ValueError:
                #     await websocket.send_json({"error": "Invalid data format"})
                #     continue

                try:
                    json_data = json.loads(data)
                    chat_data = CoachCreateChatSchema(**json_data)
                except json.JSONDecodeError:
                    chat_data = CoachCreateChatSchema(content=data)
                except ValueError:
                    await websocket.send_json({"error": "Invalid data format"})
                    continue

                saved = await self.coach_subservice.create_coach_chat(coach_id, user_id, chat_data)

                message = {
                    "content": chat_data.content,
                    "sender_type": "coach",
                    "coach_id": coach_id,
                    "user_id": user_id
                }

                # Send message to the user
                await self.user_connection_manager.send_personal_message(message, user_id)
                # Send message back to the coach (for UI consistency)
                await self.manager.send_personal_message(message, coach_id)

        except WebSocketDisconnect:
            self.manager.disconnect(coach_id, websocket)
            logger.info(f"Coach {coach_id} disconnected")

    async def get_coach_chat_history(self, user_id: int, coach_id, limit: int = 50, offset: int = 0):
        messages = await self.coach_subservice.get_coach_chat_messages(user_id, coach_id, limit, offset)
        if not messages:
            logger.info("No messages found")
            raise HTTPException(status_code=404, detail="No messages found")
        return [CoachCreateChatResponseSchema.from_orm(msg) for msg in messages]
