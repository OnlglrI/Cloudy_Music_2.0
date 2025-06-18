import pandas as pd
import os
from logger import logger

def transform(events: list[dict], csv_path: str) -> str | None:
    rows = []
    for body in events:
        try:
            user_id = int(body.get("user_id"))
            song_id = int(body.get("song_id"))
            rows.append({"user_id": user_id, "song_id": song_id})
        except (TypeError, ValueError) as e:
            logger.warning(f"❌ Ошибка преобразования данных: {e}")

    if not rows:
        logger.info("⚠️ Нет валидных данных для записи.")
        return None

    df = pd.DataFrame(rows)

    # Запись в CSV — добавляем строки без заголовка, если файл существует
    if os.path.exists(csv_path):
        df.to_csv(csv_path, mode="a", header=False, index=False)
    else:
        df.to_csv(csv_path, mode="w", header=True, index=False)

    logger.info(f"✅ Добавлено {len(rows)} строк в {csv_path}")
    return csv_path
