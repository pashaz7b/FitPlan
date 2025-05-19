# from pyexpat.errors import messages
import json
from typing import Annotated
from loguru import logger
# from fastapi import Depends, HTTPException, status
# from collections import defaultdict
# from typing import Dict
# import json

from app.domain.schemas.user_schema import (UserCreateChatSchema)
from app.subservices.user_subservice import UserSubService
from app.subservices.baseconfig import BaseService

from fastapi import WebSocket, Depends, WebSocketDisconnect
from json.decoder import JSONDecodeError
from fastapi import WebSocketDisconnect
from collections import defaultdict


class UserConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        self.active_connections[user_id].remove(websocket)

    async def send_personal_message(self, message, user_id: int):
        for websocket in self.active_connections.get(user_id, []):
            await websocket.send_json(message)


class UserMainService(BaseService):
    def __init__(self,
                 user_subservice: Annotated[UserSubService, Depends()],
                 ) -> None:
        super().__init__()
        self.user_subservice = user_subservice
        self.manager = UserConnectionManager()

    # async def user_chat_websocket(self, websocket: WebSocket, user_id: int):
    #     await self.manager.connect(user_id, websocket)
    #     try:
    #         while True:
    #             data = await websocket.receive_text()
    #             logger.info(f"message ----> {data}")
    #             chat_data = UserCreateChatSchema(content=str(data))
    #             coach = await self.user_subservice.get_user_coach(user_id)
    #             saved = await self.user_subservice.create_user_chat(user_id, coach.id, chat_data)
    #             json_data = json.loads(data)
    #             await self.manager.send_personal_message(json_data, coach.id)
    #     except WebSocketDisconnect:
    #         self.manager.disconnect(user_id, websocket)

    async def user_chat_websocket(self, websocket: WebSocket, user_id: int):
        await self.manager.connect(user_id, websocket)
        try:
            while True:
                data = await websocket.receive_text()
                logger.info(f"message ----> {data}")

                # جلوگیری از پردازش رشته خالی
                if not data.strip():
                    await websocket.send_json({"error": "empty input"})
                    continue

                try:
                    # تلاش برای تبدیل رشته به JSON
                    json_data = json.loads(data)
                    chat_data = UserCreateChatSchema(**json_data)
                except JSONDecodeError:
                    # اگر JSON نبود، فرض کن فقط متن ساده‌ست
                    chat_data = UserCreateChatSchema(content=data)
                    json_data = chat_data.dict()

                # ذخیره در دیتابیس
                coach = await self.user_subservice.get_user_coach(user_id)
                saved = await self.user_subservice.create_user_chat(user_id, coach.id, chat_data)

                # ارسال به مربی
                await self.manager.send_personal_message(json_data, coach.id)

        except WebSocketDisconnect:
            self.manager.disconnect(user_id, websocket)