import json
import logging
import asyncio
from aio_pika import IncomingMessage
from pool.es_pool import es_client
from pool.rabbit_pool import get_rabbitmq_connection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def on_message(message: IncomingMessage):
    async with message.process():
        try:
            body = json.loads(message.body.decode())
            title = body.get("title")
            artist = body.get("artist")
            album = body.get("album")
            action = body.get("action")

            if action == "add":
                doc = {"title": title, "artist": artist, "album": album}
                await es_client.index(index="songs", document=doc)
                logging.info("Песня добавлена в Elasticsearch: %s - %s", artist, title)

            elif action == "delete":
                query = {
                    "query": {
                        "bool": {
                            "must": [
                                {"match": {"title": title}},
                                {"match": {"artist": artist}},
                                {"match": {"album": album}}
                            ]
                        }
                    }
                }
                await es_client.delete_by_query(index="songs", body=query)
                logging.info("Песня удалена из Elasticsearch: %s - %s", artist, title)

            else:
                logging.warning("Неизвестное действие: %s", action)

        except Exception as e:
            logging.error("Ошибка обработки сообщения: %s", str(e))

async def main():
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    queue = await channel.declare_queue("songs.queue", durable=True)
    await queue.consume(on_message)
    logging.info("Ожидание сообщений из очереди RabbitMQ...")

    # 💥 ДЕРЖИМ КОНСЮМЕР ЖИВЫМ
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
