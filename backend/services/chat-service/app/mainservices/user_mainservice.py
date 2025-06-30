import json
from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status
# from collections import defaultdict
# from typing import Dict

from app.mainservices.singletons import get_user_connection_manager, get_coach_connection_manager
from app.domain.schemas.user_schema import (UserCreateChatSchema,
                                            UserCreateChatResponseSchema)
from app.subservices.user_subservice import UserSubService
from app.subservices.baseconfig import BaseService
from app.mainservices.connection_manager import (UserConnectionManager,
                                                 CoachConnectionManager)
from fastapi import WebSocket, Depends, WebSocketDisconnect
from json.decoder import JSONDecodeError
from fastapi import WebSocketDisconnect


# class UserConnectionManager:
#     def __init__(self):
#         self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)
#
#     async def connect(self, user_id: int, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections[user_id].append(websocket)
#
#     def disconnect(self, user_id: int, websocket: WebSocket):
#         self.active_connections[user_id].remove(websocket)
#
#     # async def send_personal_message(self, message, coach_id: int):
#     #     for websocket in self.active_connections.get(coach_id, []):
#     #         await websocket.send_json(message)
#
#     async def send_message_to_coach(self, message, coach_id: int):
#         for ws in self.active_connections.get(coach_id, []):
#             await ws.send_json(message)
#
#
# class UserMainService(BaseService):
#     def __init__(self,
#                  user_subservice: Annotated[UserSubService, Depends()],
#                  coach_connection_manager: Annotated[CoachConnectionManager, Depends()],
#                  ) -> None:
#         super().__init__()
#         self.user_subservice = user_subservice
#         self.manager = UserConnectionManager()
#         self.coach_connection_manager = coach_connection_manager
#
#     async def user_chat_websocket(self, websocket: WebSocket, user_id: int):
#         await self.manager.connect(user_id, websocket)
#         try:
#             while True:
#                 data = await websocket.receive_text()
#                 logger.info(f"message ----> {data}")
#
#                 if not data.strip():
#                     await websocket.send_json({"error": "empty input"})
#                     continue
#
#                 try:
#                     json_data = json.loads(data)
#                     chat_data = UserCreateChatSchema(**json_data)
#                 except JSONDecodeError:
#                     chat_data = UserCreateChatSchema(content=data)
#                     json_data = chat_data.dict()
#
#                 coach = await self.user_subservice.get_user_coach(user_id)
#                 saved = await self.user_subservice.create_user_chat(user_id, coach.id, chat_data)
#
#                 # await self.manager.send_personal_message(json_data, coach.id)
#                 await self.manager.send_message_to_coach(
#                     {**json_data, "sender_type": "user"}, coach.id
#                 )
#
#         except WebSocketDisconnect:
#             self.manager.disconnect(user_id, websocket)
#
#     async def get_user_chat_history(self, user_id: int, limit: int = 50, offset: int = 0):
#         coach = await self.user_subservice.get_user_coach(user_id)
#         if not coach:
#             logger.info(f"[-] No coach found for user with id ---> {user_id}")
#             raise HTTPException(status_code=404, detail="No coach found for this user")
#
#         messages = await self.user_subservice.get_user_chat_messages(user_id, coach.id, limit, offset)
#         return [UserCreateChatResponseSchema.from_orm(msg) for msg in messages]


class UserMainService:
    def __init__(
            self,
            user_subservice: Annotated[UserSubService, Depends()],
            # coach_connection_manager: Annotated[CoachConnectionManager, Depends()],
    ) -> None:
        self.user_subservice = user_subservice
        self.manager = get_user_connection_manager()
        self.coach_connection_manager = get_coach_connection_manager()

    async def user_chat_websocket(self, websocket: WebSocket, user_id: int):
        await self.manager.connect(user_id, websocket)
        try:
            while True:
                data = await websocket.receive_text()
                logger.info(f"User message from {user_id} ----> {data}")

                if not data.strip():
                    await websocket.send_json({"error": "Empty input"})
                    continue

                # try:
                #     json_data = json.loads(data)
                #     chat_data = UserCreateChatSchema(**json_data)
                # except json.JSONDecodeError:
                #     chat_data = UserCreateChatSchema(content=data)
                #     json_data = chat_data.dict()
                # except ValueError:
                #     await websocket.send_json({"error": "Invalid data format"})
                #     continue

                try:
                    json_data = json.loads(data)
                    chat_data = UserCreateChatSchema(**json_data)
                except json.JSONDecodeError:
                    chat_data = UserCreateChatSchema(content=data)
                except ValueError:
                    await websocket.send_json({"error": "Invalid data format"})
                    continue

                coach = await self.user_subservice.get_user_coach(user_id)
                if not coach:
                    await websocket.send_json({"error": "No coach assigned"})
                    continue

                # Save the chat in the database
                saved = await self.user_subservice.create_user_chat(user_id, coach.id, chat_data)

                # Prepare message
                message = {
                    "content": chat_data.content,
                    "sender_type": "user",
                    "user_id": user_id,
                    "coach_id": coach.id
                }

                # Send message to the coach
                logger.info("*************** Sending Message To Coach *************")
                await self.coach_connection_manager.send_personal_message(message, coach.id)
                logger.info("*************** Message Sended To Coach *************")
                # Send message back to the user (for UI consistency)
                await self.manager.send_personal_message(message, user_id)

        except WebSocketDisconnect:
            self.manager.disconnect(user_id, websocket)
            logger.info(f"User {user_id} disconnected")

    async def get_user_chat_history(self, user_id: int, limit: int = 50, offset: int = 0):
        coach = await self.user_subservice.get_user_coach(user_id)
        if not coach:
            logger.info(f"[-] No coach found for user with id ---> {user_id}")
            raise HTTPException(status_code=404, detail="No coach found for this user")

        messages = await self.user_subservice.get_user_chat_messages(user_id, coach.id, limit, offset)
        return [UserCreateChatResponseSchema.from_orm(msg) for msg in messages]
