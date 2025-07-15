import asyncio
import json
from aio_pika import connect_robust, IncomingMessage, ExchangeType
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.postgres_db.postgres_database import get_db
from app.domain.models.fitplan_chat_model import Admin, User, Coach
from app.infrastructure.repositories.rabbitmq import rabbitmq_repo

class RabbitmqConsumer:
    def __init__(self,):
        self.rabbitmq_url = "amqp://guest:guest@localhost/"
        self.exchange_name = "iam_chat_comm"
        self.queue_name = "id_queue"
        self.connection = None
        self.task = None
    
    async def consume(self,):
        self.connection = await connect_robust(self.rabbitmq_url)
        channel = await self.connection.channel()
        exchange = await channel.declare_exchange(self.exchange_name, ExchangeType.DIRECT)
        queue = await channel.declare_queue(self.queue_name, durable=True)
        await queue.bind(exchange, self.queue_name)
        self.task = asyncio.create_task(queue.consume(self.on_message))
        logger.info("RabbitMQ Consumer started and waiting for messages...")

    async def on_message(self, message: IncomingMessage):
        async with message.process():   # Automatically sends ack
                msg_data = json.loads(message.body)
                id = msg_data["id"]
                role = msg_data["role"]
                logger.info(f"[x] Received {role}_id: {id}")
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

    # async def start_consume(self):
        # self.setup()
        # await queue.consume(on_message)

    async def stop_consume(self):
        if self.task:
            self.task.cancel()
        if self.connection:
            await self.connection.close()
        logger.info("RabbitMQ Consumer stopped.")    


# asyncio.Future()        