# seperate worker version
import asyncio
import json
from aio_pika import connect_robust, IncomingMessage, ExchangeType
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
import signal

# fixes the ModuleNotFoundError : 'app'
import sys
import os
path = os.getcwd()
sys.path.append(path)

from app.core.postgres_db.postgres_database import get_db
from app.domain.models.fitplan_chat_model import Admin, User, Coach
from app.infrastructure.repositories.rabbitmq import rabbitmq_repo
from app.core.config.config import get_settings

rabbitmq_url = get_settings().RABBITMQ_URL
exchange_name = "iam_chat_comm"
queue_name = "id_queue"
connection = None

async def consume():
    global connection
    connection = await connect_robust(rabbitmq_url)
    channel = await connection.channel()
    exchange = await channel.declare_exchange(exchange_name, ExchangeType.DIRECT)
    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(exchange, queue_name)
    await queue.consume(on_message)
    logger.info("RabbitMQ Consumer started and waiting for messages...")

async def on_message(message: IncomingMessage):
    async with message.process():   # Automatically sends ack
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

async def stop_consume():
    if connection:
        await connection.close()
    logger.info("RabbitMQ Consumer stopped.")

shutdown_event = asyncio.Event()

def setup_signal_handlers(loop):
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: shutdown_event.set())
        
async def main():
    await consume()
    await shutdown_event.wait()
    await stop_consume()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    setup_signal_handlers(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
