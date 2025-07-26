from aio_pika import ExchangeType, DeliveryMode, connect_robust, Message
from loguru import logger
import json

from app.core.configs.config import get_settings

class RabbitmqProducer:
    def __init__(self,):
        self.rabbitmq_url = get_settings().RABBITMQ_URL
        self.exchange_name = "iam_chat_comm"
        self.queue_name = "id_queue"

    async def send_id(self, id: int, role: str):
        connection = await connect_robust(self.rabbitmq_url)
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange(self.exchange_name, ExchangeType.DIRECT)
            queue = await channel.declare_queue(self.queue_name, durable=True)
            await queue.bind(exchange, self.queue_name)

            message = json.dumps({
                "id": id,
                "role": role
            })
            await exchange.publish(
                Message(body=message.encode(), delivery_mode=DeliveryMode.PERSISTENT), 
                routing_key=self.queue_name,
            )
            logger.info(f"[.] {role}_id: {id} sent to chat-service")
        return