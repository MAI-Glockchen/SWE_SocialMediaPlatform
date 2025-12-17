FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    pillow \
    sqlmodel \
    pika

COPY . .

CMD ["python", "main.py"]
