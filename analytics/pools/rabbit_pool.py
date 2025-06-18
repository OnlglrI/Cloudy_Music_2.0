import aio_pika
import json
from config import RABBIT_URL, RABBIT_QUEUES, logger

connection = None
channel = None
exchange = None


async def init_rabbit():
    global connection, channel, exchange
    try:
        connection = await aio_pika.connect_robust(RABBIT_URL)
        channel = await connection.channel()

        # Объявляем exchange
        exchange = await channel.declare_exchange("playlist_exchange", aio_pika.ExchangeType.DIRECT)

        # Привязываем очереди к exchange
        for queue_name in RABBIT_QUEUES:
            queue = await channel.declare_queue(queue_name, durable=True)
            await queue.bind(exchange, routing_key=queue_name)
        logger.info("Connected to RabbitMQ and initialized exchange & queues")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")

async def publish_event(event: dict, queue_name: str):
    message = aio_pika.Message(
        body=json.dumps(event).encode(),
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT  # добавь это
    )
    await exchange.publish(message, routing_key=queue_name)
