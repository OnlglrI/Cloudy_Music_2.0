from minio import Minio
from minio.error import S3Error
import os
from logger import logger

MINIO_HOST = os.getenv("MINIO_HOST", "localhost")
MINIO_PORT = os.getenv("MINIO_PORT", "9000")
MINIO_USER = os.getenv("MINIO_ROOT_USER", "minio")
MINIO_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "minio123")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "analytics")

# Создаём клиент
minio_client = Minio(
    f"{MINIO_HOST}:{MINIO_PORT}",
    access_key=MINIO_USER,
    secret_key=MINIO_PASSWORD,
    secure=False  # В локальной сети — без HTTPS
)

# Проверка/создание бакета
def ensure_bucket_exists():
    found = minio_client.bucket_exists(MINIO_BUCKET)
    if not found:
        minio_client.make_bucket(MINIO_BUCKET)
        logger.info(f"Created bucket: {MINIO_BUCKET}")

# Загрузка файла
def upload_to_minio(file_path: str, object_name: str = None):
    ensure_bucket_exists()

    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        minio_client.fput_object(
            bucket_name=MINIO_BUCKET,
            object_name=object_name,
            file_path=file_path,
            content_type="text/csv"
        )
        logger.info(f"✅ Uploaded to MinIO: {object_name}")
    except S3Error as e:
        logger.warning(f"❌ Failed to upload to MinIO: {e}")
