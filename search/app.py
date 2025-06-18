from fastapi import FastAPI, HTTPException
from pool.es_pool import es_client
import logging

# Инициализация FastAPI-приложения
app = FastAPI()

# Настройка логирования на русском языке
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)


@app.get("/api/v1/search/{text}")
async def search_song(text: str):
    try:
        # Поиск по полям title, artist, album
        query = {
            "query": {
                "multi_match": {
                    "query": text,
                    "fields": ["title^3", "artist^2", "album"]
                }
            }
        }

        # Выполняем асинхронный поиск в Elasticsearch
        response = await es_client.search(index="songs", body=query)

        # Извлекаем найденные документы
        results = [hit["_source"] for hit in response["hits"]["hits"]]

        return {"results": results}

    except Exception as e:
        # Логируем ошибку и возвращаем исключение с сообщением
        logging.error("Ошибка при поиске: %s", str(e))
        raise HTTPException(status_code=500, detail="Ошибка при поиске песни")
