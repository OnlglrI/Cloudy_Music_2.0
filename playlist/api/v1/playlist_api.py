from pools.postgres_pool import get_pg_pool
from models import PlaylistCreate, SongLikeDisEvent, PlaylistUpdate, PlaylistAddDelEvent
from models import PlaylistCreate
from fastapi import FastAPI, HTTPException,APIRouter
from logger_config import logger
from sql_scripts.sql_scripts import save_playlist_to_db, add_song_playlist_to_db, delete_playlist_from_db, update_playlist_to_db, delete_songs_from_playlist_db
from pools.rabbit_pool import publish_event
from pools.redis_pool import get_redis
from datetime import datetime, UTC
import json

router = APIRouter()

@router.post("/playlist")
async def create_playlist(event: PlaylistCreate):
    event_dict = event.dict()
    redis_key = f"user:{event_dict['user_id']}:playlists"
    redis = get_redis()

    logger.info("Request received")
    custom_event = {
        "type": "playlist_service",
        "message": f"create_playlist: user_id:{event_dict['user_id']}",
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }
    try:
        logger.info(f"Sending message to RabbitMQ with values: {custom_event}")
        await publish_event(custom_event, queue_name="user.events")
        logger.info(f"Saving playlist to Postgres with values: {event_dict}")
        playlist_id = await save_playlist_to_db(event_dict)
        logger.info("Saved to Postgres")
        pipe = redis.pipeline()
        score = int(datetime.now(UTC).timestamp())
        member = json.dumps({
            "playlist_id": str(playlist_id),
            "playlist_name": event_dict["playlist_name"]
        })
        pipe.zadd(redis_key, {member: score})
        pipe.expire(redis_key, 3600)
        await pipe.execute()
        logger.info(f"Playlists for user {event_dict['user_id']} cached in Redis")

    except Exception as e:
        logger.exception("Failed to process playlist event")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"status": 200}

@router.delete("/playlist/{playlist_id}/user/{user_id}")
async def delete_playlist(playlist_id: str,user_id: str):
    logger.info("Request received")
    custom_event = {
        "type": "playlist_service",
        "message": f"delete_playlist: playlist_id:{playlist_id}",
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }
    try:
        logger.info(f"Sending message to RabbitMQ with values: {custom_event}")
        await publish_event(custom_event, queue_name="user.events")
        logger.info(f"Deleting playlist to Postgres with values: {playlist_id}")
        await delete_playlist_from_db(int(playlist_id))
        logger.info("Deleted to Postgres")

        logger.info("Deleting to Redis")
        redis_key = f"user:{user_id}:playlists"
        redis = get_redis()

        playlists = await redis.zrange(redis_key, 0, -1)

        for item in playlists:
            if str(item) == str(playlist_id):
                removed_count = await redis.zrem(redis_key, item)
                logger.info(f"Removed from Redis: {item}, count: {removed_count}")
                break
        else:
            logger.warning(f"Playlist not found in Redis ZSET for key {redis_key}")


    except Exception as e:
        logger.exception("Failed to process playlist event")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"status": 200}

@router.put("/playlist")
async def update_playlist(event: PlaylistUpdate):
    event_dict = event.dict()
    logger.info("Request received")
    custom_event = {
        "type": "playlist_service",
        "message": f"create_playlist: user_id:{event_dict['user_id']}, playlist_id:{event_dict['playlist_id']}",
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }
    try:
        logger.info(f"Sending message to RabbitMQ with values: {custom_event}")
        await publish_event(custom_event, queue_name="user.events")
        logger.info(f"Updatinge playlist to Postgres with values: {event_dict}")
        await update_playlist_to_db(event_dict)
        logger.info("Updated to Postgres")
        redis = get_redis()
        redis_key = f"user:{event_dict['user_id']}:playlists"

        # Получаем все элементы с их score
        items = await redis.zrange(redis_key, 0, -1, withscores=True)

        # Ищем нужный плейлист
        for item, score in items:
            parsed = json.loads(item)
            if str(parsed.get("playlist_id")) == str(event_dict['playlist_id']):
                # Удаляем старый member
                await redis.zrem(redis_key, item)

                # Создаём новый member с обновлённым именем
                updated_member = json.dumps({
                    "playlist_id": event_dict['playlist_id'],
                    "playlist_name": event_dict["playlist_name"]  # новое имя
                })

                # Добавляем с тем же score
                await redis.zadd(redis_key, {updated_member: int(score)})
                logger.info(f"Playlist updated in Redis ZSET with same score: {score}")
                break
        else:
            logger.warning("Playlist not found in Redis to update")

    except Exception as e:
        logger.exception("Failed to process playlist event")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"status": 200}

@router.get("playlist/user/{user_id}")
async def get_playlist(user_id: str):
    redis_key = f"user:{user_id}:playlists"
    redis = get_redis()

    custom_event = {
        "type": "playlist_service",
        "message": f"get_playlists: user_id:{user_id}",
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }

    # 2. Попытка получить из Redis
    cached_playlists = await redis.zrevrange(redis_key, 0, -1, withscores=True)
    if cached_playlists:

        logger.info(f"Sending message to RabbitMQ with values: {custom_event}")
        await publish_event(custom_event, queue_name="user.events")

        logger.info(f"Playlists for user {user_id} found in Redis")
        return [
            {
                **json.loads(member.decode() if isinstance(member, bytes) else member),
                "added_at": datetime.fromtimestamp(score, tz=UTC).isoformat()
            }
            for member, score in cached_playlists
        ]
    logger.info(f"User{user_id} playlist not found in Redis. Fetching from PostgreSQL.")
    # 3. Запрос к PostgreSQL
    query = """
        SELECT playlist_id, playlist_name, added_at
        FROM playlist.user_playlist
        WHERE user_id = $1 
        ORDER BY added_at desc
    """
    pg_pool = get_pg_pool()
    logger.info(f"Fetching from PostgreSQL.")
    async with pg_pool.acquire() as conn:
        playlists = await conn.fetch(query, int(user_id))

    if not playlists:
        raise HTTPException(status_code=404, detail="Playlist not found")

    # 4. Преобразование и сохранение в Redis (ZSET)
    pipe = redis.pipeline()
    for row in playlists:
        score = int(row["added_at"].timestamp())
        member = json.dumps({
            "playlist_id": row["playlist_id"],
            "playlist_name": row["playlist_name"]
        })
        pipe.zadd(redis_key, {member: score})
    pipe.expire(redis_key, 3600)
    await pipe.execute()
    logger.info(f"Playlists for user {user_id} cached in Redis")

    logger.info(f"Sending message to RabbitMQ with values: {custom_event}")
    await publish_event(custom_event, queue_name="user.events")

    return [
        {
            "playlist_id": row["playlist_id"],
            "playlist_name": row["playlist_name"],
            "added_at": row["added_at"].isoformat(),
        }
        for row in playlists
    ]





