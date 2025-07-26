# import asyncio
# import json
# from aio_pika import connect_robust, IncomingMessage, ExchangeType
# from loguru import logger
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.core.postgres_db.postgres_database import get_db
# from app.domain.models.fitplan_chat_model import Admin, User, Coach
# from app.infrastructure.repositories.rabbitmq import rabbitmq_repo
# from app.core.config.config import get_settings
#
# from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
#
#
# class RabbitmqConsumer:
#     def __init__(self):
#         self.rabbitmq_url = get_settings().RABBITMQ_URL
#         self.exchange_name = "iam_chat_comm"
#         self.queue_name = "id_queue"
#         self.connection = None
#         self.task = None
#
#     @retry(stop=stop_after_attempt(10), wait=wait_fixed(3))
#     async def connect(self):
#         self.connection = await connect_robust(self.rabbitmq_url)
#         logger.info("Connected to RabbitMQ")
#
#     async def consume(self):
#         try:
#             await self.connect()
#         except RetryError:
#             logger.error("Failed to connect to RabbitMQ after several attempts.")
#             return
#
#         channel = await self.connection.channel()
#         exchange = await channel.declare_exchange(self.exchange_name, ExchangeType.DIRECT)
#         queue = await channel.declare_queue(self.queue_name, durable=True)
#         await queue.bind(exchange, self.queue_name)
#
#         self.task = asyncio.create_task(queue.consume(self.on_message))
#         logger.info("RabbitMQ Consumer started and waiting for messages...")
#
#     async def on_message(self, message: IncomingMessage):
#         async with message.process():  # Automatically sends ack
#             msg_data = json.loads(message.body)
#             id = msg_data["id"]
#             role = msg_data["role"]
#             logger.info(f"[x] Received {role}_id: {id} from iam-service")
#
#             db_generator = get_db()
#             session: AsyncSession = await anext(db_generator)
#             try:
#                 match role:
#                     case "user":
#                         new_user = await rabbitmq_repo.add_user(session, User(id=id))
#                         logger.info(f"[+] User Created With Id ---> {new_user.id}")
#                     case "coach":
#                         new_coach = await rabbitmq_repo.add_coach(session, Coach(id=id))
#                         logger.info(f"[+] Coach Created With Id ---> {new_coach.id}")
#                     case "admin":
#                         new_admin = await rabbitmq_repo.add_admin(session, Admin(id=id))
#                         logger.info(f"[+] Admin Created With Id ---> {new_admin.id}")
#                     case _:
#                         logger.warning(f"Unknown role received: {role}")
#             finally:
#                 await db_generator.aclose()
#
#     async def stop_consume(self):
#         if self.task:
#             self.task.cancel()
#         if self.connection:
#             await self.connection.close()
#         logger.info("RabbitMQ Consumer stopped.")

import asyncio
import json
from aio_pika import connect_robust, IncomingMessage, ExchangeType
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.postgres_db.postgres_database import get_db
from app.domain.models.fitplan_chat_model import Admin, User, Coach, UserCoachWith
from app.infrastructure.repositories.rabbitmq import rabbitmq_repo
from app.core.config.config import get_settings

from tenacity import retry, stop_after_attempt, wait_fixed, RetryError


class RabbitmqConsumer:
    def __init__(self):
        self.rabbitmq_url = get_settings().RABBITMQ_URL
        self.connection = None
        self.tasks = []

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(3))
    async def connect(self):
        self.connection = await connect_robust(self.rabbitmq_url)
        logger.info("Connected to RabbitMQ")

    async def consume_all(self):
        try:
            await self.connect()
        except RetryError:
            logger.error("Failed to connect to RabbitMQ after several attempts.")
            return

        channel = await self.connection.channel()

        # Queue: iam_chat_comm
        exchange_iam = await channel.declare_exchange("iam_chat_comm", ExchangeType.DIRECT)
        queue_iam = await channel.declare_queue("id_queue", durable=True)
        await queue_iam.bind(exchange_iam, "id_queue")
        self.tasks.append(asyncio.create_task(queue_iam.consume(self.on_iam_message)))

        # Queue: core_chat_comm
        exchange_core = await channel.declare_exchange("core_chat_comm", ExchangeType.DIRECT)
        queue_core = await channel.declare_queue("id_id_queue", durable=True)
        await queue_core.bind(exchange_core, "id_id_queue")
        self.tasks.append(asyncio.create_task(queue_core.consume(self.on_core_message)))

        logger.info("RabbitMQ Consumer started. Listening on iam_chat_comm and core_chat_comm...")

    async def on_iam_message(self, message: IncomingMessage):
        async with message.process():
            msg_data = json.loads(message.body)
            id = msg_data["id"]
            role = msg_data["role"]
            logger.info(f"[x] Received {role}_id: {id} from iam-service")

            db_generator = get_db()
            session: AsyncSession = await anext(db_generator)
            try:
                match role:
                    case "user":
                        new_user = await rabbitmq_repo.add_user(session, User(id=id))
                        logger.info(f"[+] User Created With Id ---> {new_user.id}")
                    case "coach":
                        new_coach = await rabbitmq_repo.add_coach(session, Coach(id=id))
                        logger.info(f"[+] Coach Created With Id ---> {new_coach.id}")
                    case "admin":
                        new_admin = await rabbitmq_repo.add_admin(session, Admin(id=id))
                        logger.info(f"[+] Admin Created With Id ---> {new_admin.id}")
                    case _:
                        logger.warning(f"Unknown role received: {role}")
            finally:
                await db_generator.aclose()

    async def on_core_message(self, message: IncomingMessage):
        async with message.process():
            msg_data = json.loads(message.body)
            user_id = msg_data["user_id"]
            coach_id = msg_data["coach_id"]
            role = msg_data["role"]

            logger.info(f"[x] Received from core_chat_comm → user_id: {user_id}, coach_id: {coach_id}, role: {role}")

            db_generator = get_db()
            session: AsyncSession = await anext(db_generator)
            try:
                match role:
                    case "user_coach_create":
                        new_user_coach_with = await rabbitmq_repo.add_user_coach_with(session, UserCoachWith(
                            user_id=user_id,
                            coach_id=coach_id
                        ))
                        logger.info(f"[+] UserCoachWith Created")
                    case "user_coach_change":
                        user_coach_with_dict = {"user_id": user_id, "new_coach_id": coach_id}
                        new_coach = await rabbitmq_repo.change_user_coach(session, user_coach_with_dict)
                        logger.info(f"[+] Coach Changed With Id ---> {coach_id}")
                    case _:
                        logger.warning(f"Unknown role received: {role}")
            finally:
                await db_generator.aclose()

            # async for session in get_db():
            #     async with session.begin():
            #         match role:
            #             case "user_coach_create":
            #                 await rabbitmq_repo.add_user_coach_with(session, UserCoachWith(
            #                     user_id=user_id,
            #                     coach_id=coach_id
            #                 ))
            #                 logger.info(f"[+] UserCoachWith Created")
            #             case "user_coach_change":
            #                 pass
            #             case _:
            #                 logger.warning(f"Unknown role received: {role}")
            #     break

    async def stop_consume(self):
        for task in self.tasks:
            task.cancel()
        if self.connection:
            await self.connection.close()
        logger.info("RabbitMQ Consumer stopped.")
