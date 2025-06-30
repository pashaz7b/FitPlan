from collections import defaultdict
from fastapi import WebSocket
from typing import Dict, List
from loguru import logger


#
# class CoachConnectionManager:
#     def __init__(self):
#         self.active_connections: Dict[int, List[WebSocket]] = defaultdict(list)
#
#     async def connect(self, coach_id: int, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections[coach_id].append(websocket)
#
#     def disconnect(self, coach_id: int, websocket: WebSocket):
#         if coach_id in self.active_connections:
#             self.active_connections[coach_id].remove(websocket)
#             if not self.active_connections[coach_id]:
#                 del self.active_connections[coach_id]
#
#     async def send_personal_message(self, message: dict, coach_id: int):
#         for websocket in self.active_connections.get(coach_id, []):
#             await websocket.send_json(message)
#
#
# class UserConnectionManager:
#     def __init__(self):
#         self.active_connections: Dict[int, List[WebSocket]] = defaultdict(list)
#
#     async def connect(self, user_id: int, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections[user_id].append(websocket)
#
#     def disconnect(self, user_id: int, websocket: WebSocket):
#         if user_id in self.active_connections:
#             self.active_connections[user_id].remove(websocket)
#             if not self.active_connections[user_id]:
#                 del self.active_connections[user_id]
#
#     async def send_personal_message(self, message: dict, user_id: int):
#         for websocket in self.active_connections.get(user_id, []):
#             await websocket.send_json(message)


class CoachConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = defaultdict(list)

    async def connect(self, coach_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[coach_id].append(websocket)
        logger.info(f"Coach {coach_id} connected. Active connections: {len(self.active_connections[coach_id])}")

    def disconnect(self, coach_id: int, websocket: WebSocket):
        if coach_id in self.active_connections:
            self.active_connections[coach_id].remove(websocket)
            logger.info(f"Coach {coach_id} disconnected. Active connections: {len(self.active_connections[coach_id])}")
            if not self.active_connections[coach_id]:
                del self.active_connections[coach_id]

    async def send_personal_message(self, message: dict, coach_id: int):
        logger.info(f"Sending message to coach {coach_id}: {message}")
        logger.info(f"Current coach connections keys: {list(self.active_connections.keys())}")
        for websocket in self.active_connections.get(coach_id, []):
            print(f"WEEBBBBB SOCKET {websocket} ------------ {message}")
            await websocket.send_json(message)
            logger.info(f"Message sent to coach {coach_id} via websocket")


class UserConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = defaultdict(list)

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected. Active connections: {len(self.active_connections[user_id])}")

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            logger.info(f"User {user_id} disconnected. Active connections: {len(self.active_connections[user_id])}")
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: int):
        logger.info(f"Sending message to user {user_id}: {message}")
        for websocket in self.active_connections.get(user_id, []):
            await websocket.send_json(message)
            logger.info(f"Message sent to user {user_id} via websocket")
