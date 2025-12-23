FROM python:3.11-slim

WORKDIR /app


# Python deps
RUN pip install requests pika dotenv


COPY . .

CMD ["python", "consumer.py"]
