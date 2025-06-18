from pools.postgres_pool import get_pg_pool
from models import PlaylistCreate, SongLikeDisEvent, PlaylistUpdate, PlaylistAddDelEvent
from models import PlaylistCreate
from fastapi import FastAPI, HTTPException, APIRouter
from logger_config import logger
from sql_scripts.sql_scripts import delete_songs_from_dislikes_db, add_song_dislikes_to_db
from pools.rabbit_pool import publish_event
from pools.redis_pool import get_redis
from datetime import datetime, UTC
import json

router = APIRouter()


@router.get("/playlist/dislikes/user/{user_id}")
async def get_songs_from_dislikes(user_id: str):
    redis_key = f"dislikes:{user_id}:songs"
    redis = get_redis()
    custom_event = {
        "type": "playlist_service",
        "message": f"get_songs_of_dislikes: user_id:{user_id}",
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }

    cached_songs = await redis.zrevrange(redis_key, 0, -1, withscores=True)
    if cached_songs:

        logger.info(f"Sending message to RabbitMQ with values: {custom_event}")
        await publish_event(custom_event, queue_name="user.events")

        logger.info(f"User {user_id} found in Redis")
        return [
            {
                "song_id": int(song_id.decode() if isinstance(song_id, bytes) else song_id),
            }
            for song_id, score in cached_songs
        ]

    logger.info(f"User {user_id} not found in Redis. Fetching from PostgreSQL.")

    logger.info(f"Sending message to RabbitMQ with values: {custom_event}")
    await publish_event(custom_event, queue_name="user.events")

    query = """
        SELECT song_id, added_at
        FROM playlist.disliked_songs
        WHERE user_id = $1 
        ORDER BY added_at desc
    """
    pg_pool = get_pg_pool()
    logger.info(f"Fetching from PostgreSQL.")
    async with pg_pool.acquire() as conn:
        songs = await conn.fetch(query, int(user_id))

    if not songs:
        raise HTTPException(status_code=404, detail="Song not found")

    logger.info(f"User {user_id} put in Redis.")
    pipe = redis.pipeline()
    for row in songs:
        score = int(row["added_at"].timestamp())
        member = str(row["song_id"])
        pipe.zadd(redis_key, {member: score})
    pipe.expire(redis_key, 3600)
    await pipe.execute()

    return [
        {
            "song_id": row["song_id"],
        }
        for row in songs
    ]


@router.post("/playlist/dislikes")
async def add_song_to_dislikes(event: SongLikeDisEvent):
    event_dict = event.dict()
    redis_key = f"dislikes:{event_dict['user_id']}:songs"
    redis = get_redis()
    logger.info("Request received")
    custom_event = {
        "type": "playlist_service",
        "message": f"add_song_to_dislikes: user_id:{event_dict['user_id']}, song_id:{event_dict['song_id']}",
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }
    try:
        logger.info(f"Sending message to RabbitMQ with values: {custom_event}")
        await publish_event(custom_event, queue_name="user.events")
        logger.info(f"Saving song to Postgres.dislikes with values: {event_dict}")
        await add_song_dislikes_to_db(event_dict)
        logger.info("Saved to Postgres.dislikes")

        pipe = redis.pipeline()
        score = int(datetime.now(UTC).timestamp())
        member = str(event_dict["song_id"])
        pipe.zadd(redis_key, {member: score})
        pipe.expire(redis_key, 3600)
        await pipe.execute()
        logger.info(f"User {event_dict['user_id']} put in Redis.")

    except Exception as e:
        logger.exception("Failed to process playlist event")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"status": 200}

@router.delete("/playlist/dislikes/user/{user_id}/song/{song_id}")
async def delete_song_from_dislikes(song_id: str, user_id: str):
    logger.info("Request received")
    custom_event = {
        "type": "playlist_service",
        "message": f"add_song_to_dislikes: user_id:{user_id}, song_id:{song_id}",
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }
    try:
        logger.info(f"Sending message to RabbitMQ with values: {custom_event}")
        await publish_event(custom_event, queue_name="user.events")
        logger.info(f"Deleting song from Postgres.dislikes with values: {user_id}:{song_id}")
        await delete_songs_from_dislikes_db(int(song_id), int(user_id))
        logger.info("Deleted from Postgres.dislikes")
        logger.info("Deleting from Redis")
        # Удаление из Redis ZSET
        redis_key = f"dislikes:{user_id}:songs"

        redis = get_redis()

        # Получаем все элементы ZSET
        songs = await redis.zrange(redis_key, 0, -1)

        # Ищем нужный элемент
        for item in songs:
            if str(item) == str(song_id):
                removed_count = await redis.zrem(redis_key, item)
                logger.info(f"Removed from Redis: {item}, count: {removed_count}")
                break
        else:
            logger.warning(f"Song not found in Redis ZSET for key {redis_key}")
    except Exception as e:
        logger.exception("Failed to process playlist event")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"status": 200}
