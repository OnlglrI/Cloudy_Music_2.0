# ./rabbit_init/init_queues.py
import pika
import os
import time
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "guest")

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)

for i in range(10):
    try:
        connection = pika.BlockingConnection(parameters)
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"🔁 [{i+1}/10] RabbitMQ ещё не готов. Ожидание 10 сек...")
        time.sleep(10)
else:
    print("❌ Не удалось подключиться к RabbitMQ после 10 попыток")
    exit(1)

channel = connection.channel()

channel.queue_declare(queue='songs.queue', durable=True)        # для elasticsearch сообщение с методанными песни для добавление в elasticsearch
print("✅ Очередь 1 'songs.queue' готова")
channel.queue_declare(queue='user.events', durable=True)         # для analytics события которые делают пользователи
print("✅ Очередь 2 'user.events' готова")
channel.queue_declare(queue='recomdation.send', durable=True)   # для user сообщение которое говорит что рекомендации добавлены в minio и где они лежат
print("✅ Очередь 3 'recomdation.send' готова")
# RABBIT_QUEUES = ["playlist_queue", "favorites_queue", "dislikes_queue", "playlist-user_queue"]
