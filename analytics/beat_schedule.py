from celery.schedules import crontab

beat_schedule = {
    "run-extract-every-5-minutes": {
        "task": "analytics.tasks.run_extract",
        "schedule": crontab(minute="*/5"),
    },
    "run-analytics-every-day": {
        "task": "analytics.tasks.run_analytics",
        "schedule": crontab(hour=0, minute=0),
    },
}
