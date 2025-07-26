from aio_pika import ExchangeType, DeliveryMode, connect_robust, Message
from loguru import logger
import json

from app.core.config.config import get_settings


class RabbitmqProducer:
    def __init__(self, ):
        self.rabbitmq_url = get_settings().RABBITMQ_URL
        self.exchange_name = "core_chat_comm"
        self.queue_name = "id_id_queue"

    async def send_id(self, user_id: int, coach_id: int, role: str):
        connection = await connect_robust(self.rabbitmq_url)
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange(self.exchange_name, ExchangeType.DIRECT)
            queue = await channel.declare_queue(self.queue_name, durable=True)
            await queue.bind(exchange, self.queue_name)

            message = json.dumps({
                "user_id": user_id,
                "coach_id": coach_id,
                "role": role
            })
            await exchange.publish(
                Message(body=message.encode(), delivery_mode=DeliveryMode.PERSISTENT),
                routing_key=self.queue_name,
            )
            logger.info(f"[.] message has been sent to chat-service")
        return
