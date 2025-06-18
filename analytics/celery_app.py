from celery import Celery
import os
from config import RABBIT_URL
from beat_schedule import beat_schedule

celery_app = Celery(
    "analytics",
    broker=os.getenv("CELERY_BROKER_URL", RABBIT_URL),
    backend=os.getenv("CELERY_RESULT_BACKEND", "rpc://"),
    include=["tasks"]
)

celery_app.conf.beat_schedule = beat_schedule
celery_app.conf.timezone = "UTC"
