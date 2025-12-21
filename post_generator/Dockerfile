FROM python:3.13-slim

WORKDIR /app



RUN pip install --no-cache-dir \
    requests \
    pika

RUN pip install --no-cache-dir "transformers>=4.57.3,<5.0.0" "torch>=2.9.1,<3.0.0" ;

COPY . .

CMD ["python", "consumer.py"]
