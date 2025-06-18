from pools.postgres_pool import get_pg_pool
from models import PlaylistCreate, SongLikeDisEvent, PlaylistUpdate, PlaylistAddDelEvent
from models import PlaylistCreate
from fastapi import FastAPI, HTTPException, APIRouter
from logger_config import logger
from sql_scripts.sql_scripts import add_song_playlist_to_db, delete_songs_from_playlist_db
from pools.rabbit_pool import publish_event
from pools.redis_pool import get_redis
from datetime import datetime, UTC
import json


router = APIRouter()


@router.get("/playlist/{playlist_id}")
async def get_songs_from_playlist(playlist_id: str):
    redis_key = f"playlist:{playlist_id}:songs"
    redis = get_redis()
    custom_event = {
        "type": "playlist_service",
        "message": f"get_songs_of_playlist: playlist_id:{playlist_id}",
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }

    cached_songs = await redis.zrevrange(redis_key, 0, -1, withscores=True)
    if cached_songs:

        logger.info(f"Sending message to RabbitMQ with values: {custom_event}")
        await publish_event(custom_event, queue_name="user.events")

        logger.info(f"Playlist {playlist_id} found in Redis")
        return [
            {
                "song_id": int(song_id.decode() if isinstance(song_id, bytes) else song_id),
            }
            for song_id, score in cached_songs
        ]

    logger.info(f"Playlist {playlist_id} not found in Redis. Fetching from PostgreSQL.")

    logger.info(f"Sending message to RabbitMQ with values: {custom_event}")
    await publish_event(custom_event, queue_name="user.events")

    query = """
        SELECT song_id, added_at
        FROM playlist.playlist_songs
        WHERE playlist_id = $1 
        ORDER BY added_at desc
    """
    pg_pool = get_pg_pool()
    logger.info(f"Fetching from PostgreSQL.")
    async with pg_pool.acquire() as conn:
        songs = await conn.fetch(query, int(playlist_id))

    if not songs:
        raise HTTPException(status_code=404, detail="Song not found")

    logger.info(f"Playlist {playlist_id} put in Redis.")
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


@router.post("/playlist/song")
async def add_song_to_playlist(event: PlaylistAddDelEvent):
    event_dict = event.dict()
    redis_key = f"playlist:{event_dict['playlist_id']}:songs"
    redis = get_redis()
    logger.info("Request received")
    custom_event = {
        "type": "playlist_service",
        "message": f"add_song_to_playlist: playlist_id:{event_dict['playlist_id']}, song_id:{event_dict['song_id']}",
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }
    try:
        logger.info(f"Sending message to RabbitMQ with values: {custom_event}")
        await publish_event(custom_event, queue_name="user.events")
        logger.info(f"Saving song to Postgres with values: {event_dict}")
        await add_song_playlist_to_db(event_dict)
        logger.info("Saved to Postgres")

        logger.info(f"Playlist {event_dict['playlist_id']} put in Redis.")
        pipe = redis.pipeline()
        score = int(datetime.now(UTC).timestamp())
        member = str(event_dict["song_id"])
        pipe.zadd(redis_key, {member: score})
        pipe.expire(redis_key, 3600)
        await pipe.execute()
    except Exception as e:
        logger.exception("Failed to process playlist event")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"status": 200}


@router.delete("/playlist/{playlist_id}/song/{song_id}")
async def delete_song_from_playlist(song_id: str, playlist_id: str):
    logger.info("Request received")
    custom_event = {
        "type": "playlist_service",
        "message": f"add_song_to_playlist: playlist_id:{playlist_id}, song_id:{song_id}",
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }
    try:
        logger.info(f"Sending message to RabbitMQ with values: {custom_event}")
        await publish_event(custom_event, queue_name="user.events")
        logger.info(f"Deleting song from Postgres with values: {playlist_id}:{song_id}")
        await delete_songs_from_playlist_db(int(song_id), int(playlist_id))
        logger.info("Deleting from Redis")
        # Удаление из Redis ZSET
        redis_key = f"playlist:{playlist_id}:songs"

        redis = get_redis()

        # Получаем все элементы ZSET
        playlists = await redis.zrange(redis_key, 0, -1)

        # Ищем нужный элемент
        for item in playlists:
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