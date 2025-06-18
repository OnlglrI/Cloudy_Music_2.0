from datetime import datetime, timezone
import os
import pandas as pd
from ETL.load import upload_to_minio
from config import RABBIT_QUEUES
from logger import logger

RAW_DIR = "storage/raw"
PROCESSED_DIR = "storage/processed"

def aggregate_and_load():
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    raw_file = f"{RAW_DIR}/{RABBIT_QUEUES[0]}_{date_str}.csv"
    agg_file = f"{PROCESSED_DIR}/aggregated_{date_str}.csv"

    if not os.path.exists(raw_file):
        logger.warning(f"❌ Файл не найден: {raw_file}")
        return

    df = pd.read_csv(raw_file)

    agg = df.groupby("user_id").agg({"song_id": "count"}).reset_index()
    agg.rename(columns={"song_id": "songs_listened"}, inplace=True)

    agg.to_csv(agg_file, index=False)
    logger.info(f"✅ Aggregated: {agg_file}")

    upload_to_minio(agg_file, object_name=f"aggregated/{date_str}.csv")

    os.remove(raw_file)
    os.remove(agg_file)
    logger,info("🧹 Удалены временные файлы")

if __name__ == "__main__":
    aggregate_and_load()