import asyncio
import json
from datetime import datetime, timezone
from aio_pika import connect_robust
from config import RABBIT_URL, RABBIT_QUEUES
from ETL.transform import transform
from logger import logger

SAVE_DIR = "storage/raw"
FILENAME_TEMPLATE = "{queue}_{date}.csv"

async def fetch_messages_from_queue(queue_name: str):
    connection = await connect_robust(RABBIT_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name, durable=True)

    messages = []
    while True:
        message = await queue.get(no_ack=False, fail=False)
        if message is None:
            break

        try:
            body = json.loads(message.body.decode())
            messages.append(body)
            await message.ack()
        except Exception as e:
            logger.error(f"❌ Error decoding message from {queue_name}: {e}")
            await message.nack(requeue=False)

    await connection.close()
    return messages


async def process_queue(queue_name: str):
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filename = FILENAME_TEMPLATE.format(queue=queue_name, date=date_str)
    filepath = f"{SAVE_DIR}/{filename}"

    events = await fetch_messages_from_queue(queue_name)
    if events:
        transform(events, filepath)
        logger.info(f"✅ Processed {len(events)} messages from {queue_name} and saved to {filepath}")
    else:
        logger.info(f"ℹ️ No messages in {queue_name}")


async def main():
    await asyncio.gather(*(process_queue(q) for q in RABBIT_QUEUES))


if __name__ == "__main__":
    asyncio.run(main())


