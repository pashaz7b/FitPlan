from aio_pika import ExchangeType, DeliveryMode, connect_robust, Message
from loguru import logger

class RabbitmqProducer:
    def __init__(self,):
        self.rabbitmq_url = "amqp://guest:guest@localhost/"
        self.exchange_name = "iam_chat_comm"
        self.queue_name = "user_id_queue"

    async def send_user_id(self, user_id: int):
        connection = await connect_robust(self.rabbitmq_url)
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange(self.exchange_name, ExchangeType.DIRECT)
            queue = await channel.declare_queue(self.queue_name, durable=True)
            await queue.bind(exchange, self.queue_name)
            await exchange.publish(
                Message(body=str(user_id).encode(), delivery_mode=DeliveryMode.PERSISTENT), 
                routing_key=self.queue_name,
            )
            logger.info(f"[.] User ID {user_id} sent to chat service")
        return     