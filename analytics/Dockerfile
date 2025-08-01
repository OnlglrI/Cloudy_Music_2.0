FROM python:3.11-slim

WORKDIR /app

COPY requiments.txt ./
RUN pip install --no-cache-dir -r requiments.txt

COPY . ./
ENV PYTHONUNBUFFERED=1

CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]
