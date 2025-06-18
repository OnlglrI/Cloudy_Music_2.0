from redis.asyncio import Redis
from config import REDIS_URL
from logger_config import logger


redis = None

async def init_redis():
    global redis
    redis = await Redis.from_url(REDIS_URL, decode_responses=True)
    try:
        await redis.ping()
        logger.info("Connected to Redis")
    except Exception as e:
        logger.info(f"Failed to connect to Redis: {e}")


def get_redis() -> Redis:
    if redis is None:
        raise RuntimeError("Redis has not been initialized")
    return redis