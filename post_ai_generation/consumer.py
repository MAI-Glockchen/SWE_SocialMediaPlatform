import json
import os
import time
import traceback

import pika
import requests
from text_generator_mistral import MistralTextGenerator

RABBIT_HOST = os.environ.get("RABBIT_HOST", "localhost")
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

QUEUE_POSTS = "posts.generate"
QUEUE_COMMENTS = "comments.generate"

# Importiere erst nach Verfügbarkeit aller ML-Dependencies
print("[post-generator] Starting consumer before imports", flush=True)


text_gen = MistralTextGenerator()


def process_post(ch, method, properties, body):
    try:
        msg = json.loads(body)
        user = msg.get("user", "AI User")
        prompt = msg.get("prompt", "")
        persona = msg.get("persona", "neutral")
        image = msg.get("image")

        print(f"[post-generator] Generating post for user={user} persona={persona}")
        text = text_gen.generate_text(additional_prompt=prompt, persona=persona)

        payload = {"user": user, "text": text, "image": image}
        resp = requests.post(f"{BACKEND_URL}/posts/", json=payload, timeout=30)
        resp.raise_for_status()

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("[post-generator] Post created")
    except Exception as e:
        print("[post-generator] Error processing post:", e)
        traceback.print_exc()
        try:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception:
            pass


def process_comment(ch, method, properties, body):
    try:
        msg = json.loads(body)
        post_text = msg.get("post_text")
        post_id = msg.get("post_id")
        user = msg.get("user", "AI User")
        persona = msg.get("persona", "neutral")

        if not post_text:
            raise ValueError("missing post_text in message")

        print(f"[post-generator] Generating comment for post with persona={persona}")
        text = text_gen.generate_text(additional_prompt=post_text, persona=persona)

        payload = {"user": user, "text": text}
        resp = requests.post(f"{BACKEND_URL}/posts/{post_id}/comments", json=payload, timeout=30)
        resp.raise_for_status()

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("[post-generator] Comment created")
    except Exception as e:
        print("[post-generator] Error processing comment:", e)
        traceback.print_exc()
        try:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception:
            pass


def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_POSTS, durable=True)
    channel.queue_declare(queue=QUEUE_COMMENTS, durable=True)

    channel.basic_consume(queue=QUEUE_POSTS, on_message_callback=process_post, auto_ack=False)
    channel.basic_consume(queue=QUEUE_COMMENTS, on_message_callback=process_comment, auto_ack=False)

    print("[post-generator] Waiting for messages...", flush=True)
    channel.start_consuming()


def main():
    retry_delay = 1
    while True:
        try:
            print(f"[post-generator] Connecting to RabbitMQ at {RABBIT_HOST}...", flush=True)
            consume()
            retry_delay = 1
        except Exception as e:
            print(f"[post-generator] Connection lost: {e}, retrying in {retry_delay}s", flush=True)
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)


if __name__ == "__main__":
    print("[post-generator] Starting consumer...", flush=True)
    main()

print("[post-generator] Starting consumer outside of main...", flush=True)
