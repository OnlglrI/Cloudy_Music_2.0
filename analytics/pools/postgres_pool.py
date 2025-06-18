import asyncpg
from config import POSTGRES_URL, logger

pg_pool = None

async def init_pg():
    logger.info('Create connected PostgreSQL pool')
    global pg_pool
    pg_pool = await asyncpg.create_pool(dsn=POSTGRES_URL)

def get_pg_pool():
    if pg_pool is None:
        raise RuntimeError("Postgres has not been initialized")
    return pg_pool