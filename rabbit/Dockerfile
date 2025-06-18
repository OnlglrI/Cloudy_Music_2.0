# ./rabbit_init/Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY init_queues.py .

RUN pip install pika

CMD ["python", "init_queues.py"]
