FROM python:3.13-slim

WORKDIR /app


# Python deps
RUN pip install requests pika dotenv


COPY . .

CMD ["python", "consumer.py"]
