import asyncio
import json
from aio_pika import connect_robust, IncomingMessage, ExchangeType
from loguru import logger

class RabbitmqConsumer:
    def __init__(self,):
        # self.user_subservice = user_subservice
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
                # process message: create user, coach, admin in db
                # await self.user_subservice.create_user(user_id)

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