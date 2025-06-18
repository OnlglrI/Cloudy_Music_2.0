from fastapi import FastAPI
from api.v1 import playlist_api, dislikes_api, favorites_api, songs_api
from pools.rabbit_pool import init_rabbit
from pools.redis_pool import init_redis
from pools.postgres_pool import init_pg
from middleware import TraceIDMiddleware
from logger_config import logger  # инициализация логгера
import uvicorn

app = FastAPI()

app.add_middleware(TraceIDMiddleware)

# Подключаем роутеры
app.include_router(playlist_api.router, prefix="/api/v1", tags=["playlist"])
app.include_router(dislikes_api.router, prefix="/api/v1", tags=["dislikes"])
app.include_router(favorites_api.router, prefix="/api/v1", tags=["favorites"])
app.include_router(songs_api.router, prefix="/api/v1", tags=["songs"])

@app.on_event("startup")
async def startup():
    logger.info("Starting up connections")
    await init_pg()
    await init_redis()
    await init_rabbit()

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
