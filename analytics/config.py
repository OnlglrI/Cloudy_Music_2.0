import os
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# Redis
REDIS_PORT=os.getenv("REDIS_PORT")
REDIS_HOST=os.getenv("REDIS_HOST")
# RabbitMQ
RABBITMQ_PORT=os.getenv("RABBITMQ_PORT")
RABBITMQ_MANAGEMENT_PORT=os.getenv("RABBITMQ_MANAGEMENT_PORT")
RABBITMQ_USER=os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD=os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_HOST=os.getenv("RABBITMQ_HOST")

# PostgreSQL
POSTGRES_PORT=os.getenv("POSTGRES_PORT")
POSTGRES_USER="playlist_user"
POSTGRES_PASSWORD="playlist_password"
POSTGRES_DB="playlist_db"
POSTGRES_HOST=os.getenv("POSTGRES_HOST")

RABBIT_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}/"
POSTGRES_URL="postgresql://playlist_user:playlist_password@postgres:5432/playlist_db"
# POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
REDIS_URL = f"redis://{REDIS_HOST}"
RABBIT_QUEUES = ["playlist_queue", "favorites_queue", "dislikes_queue", "playlist-user_queue"]
# POSTGRES_URL = "postgresql+psycopg2://playlist_user:playlist_password@postgres:5432/musicapp"
