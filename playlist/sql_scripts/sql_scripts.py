from logger_config import logger
from pools.postgres_pool import get_pg_pool



async def add_song_playlist_to_db(event_dict: dict):
    query = """
        INSERT INTO playlist.playlist_songs ( playlist_id, song_id)
        VALUES ($1, $2)
    """
    pg_pool = get_pg_pool()

    async with pg_pool.acquire() as conn:
        await conn.execute(
            query,
            int(event_dict["playlist_id"]),
            int(event_dict["song_id"]),
        )

async def add_song_favorites_to_db(event_dict: dict):
    query = """
        INSERT INTO playlist.favorite_songs ( user_id, song_id)
        VALUES ($1, $2)
    """
    pg_pool = get_pg_pool()

    async with pg_pool.acquire() as conn:
        await conn.execute(
            query,
            int(event_dict["user_id"]),
            int(event_dict["song_id"]),
        )

async def add_song_dislikes_to_db(event_dict: dict):
    query = """
        INSERT INTO playlist.disliked_songs ( user_id, song_id)
        VALUES ($1, $2)
    """
    pg_pool = get_pg_pool()

    async with pg_pool.acquire() as conn:
        await conn.execute(
            query,
            int(event_dict["user_id"]),
            int(event_dict["song_id"]),
        )

async def update_playlist_to_db(event_dict: dict):
    query = """
        UPDATE playlist.user_playlist
        SET playlist_name = $2
        WHERE playlist_id = $1
        AND user_id = $3
    """
    pg_pool = get_pg_pool()

    async with pg_pool.acquire() as conn:
        await conn.execute(
            query,
            int(event_dict["playlist_id"]),
            event_dict["playlist_name"],
            int(event_dict["user_id"]),
        )


async def delete_playlist_from_db(playlist_id: int):
    query = """
        DELETE FROM playlist.user_playlist
        WHERE playlist_id = $1
    """
    pg_pool = get_pg_pool()
    async with pg_pool.acquire() as conn:
        await conn.execute(query, playlist_id)
        logger.info(f"Deleted playlist with id: {playlist_id}")


async def save_playlist_to_db(event_dict: dict) -> int:
    query = """
        INSERT INTO playlist.user_playlist (user_id, playlist_name)
        VALUES ($1, $2)
        RETURNING playlist_id
    """
    pg_pool = get_pg_pool()

    async with pg_pool.acquire() as conn:
        row = await conn.fetchrow(
            query,
            int(event_dict["user_id"]),
            event_dict["playlist_name"],
        )
        return row["playlist_id"]


async def delete_songs_from_playlist_db(song_id: int, playlist_id: int):
    query = """
        DELETE FROM playlist.playlist_songs
        WHERE playlist_id = $1
        AND song_id = $2
    """
    pg_pool = get_pg_pool()
    async with pg_pool.acquire() as conn:
        await conn.execute(query, playlist_id, song_id)
        logger.info(f"Deleted song with id: {song_id}, playlist_id: {playlist_id}")

async def delete_songs_from_favorites_db(song_id: int, user_id: int):
    query = """
        DELETE FROM playlist.favorite_songs
        WHERE user_id = $1
        AND song_id = $2
    """
    pg_pool = get_pg_pool()
    async with pg_pool.acquire() as conn:
        await conn.execute(query, user_id, song_id)
        logger.info(f"Deleted song with id: {song_id}, user_id: {user_id}")

async def delete_songs_from_dislikes_db(song_id: int, user_id: int):
    query = """
        DELETE FROM playlist.disliked_songs
        WHERE user_id = $1
        AND song_id = $2
    """
    pg_pool = get_pg_pool()
    async with pg_pool.acquire() as conn:
        await conn.execute(query, user_id, song_id)
        logger.info(f"Deleted song with id: {song_id}, user_id: {user_id}")
