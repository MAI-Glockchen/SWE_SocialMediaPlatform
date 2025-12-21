import json
import os
import time
import traceback

import pika
import requests

RABBIT_HOST = os.environ.get("RABBIT_HOST", "rabbitmq")
BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")
QUEUE_POSTS = "posts.generate"
QUEUE_COMMENTS = "comments.generate"

# Always use the real TextGenerator; fail fast if it's unavailable
try:
    from generator import TextGenerator
except Exception as e:
    print("[consumer] Failed to import TextGenerator from post_generator.generator:", e)
    print(
        "[consumer] Make sure to build the image with ML dependencies or install them in your env."
    )
    raise

text_gen = TextGenerator()


def process_post(ch, method, properties, body):
    try:
        msg = json.loads(body)
        user = msg.get("user", "AI User")
        prompt = msg.get("prompt", "")
        persona = msg.get("persona", "neutral")
        image = msg.get("image")

        print(f"[consumer] Generating post for user={user} persona={persona}")
        text = text_gen.generate_text(additional_prompt=prompt, persona=persona)

        payload = {"user": user, "text": text, "image": image}
        resp = requests.post(f"{BACKEND_URL}/posts/", json=payload, timeout=30)
        resp.raise_for_status()

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("[consumer] Post created via backend")
    except Exception as e:
        print("[consumer] Error processing post job:", e)
        traceback.print_exc()
        try:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception:
            pass


def process_comment(ch, method, properties, body):
    try:
        msg = json.loads(body)
        post_id = msg.get("post_id")
        user = msg.get("user", "AI User")
        persona = msg.get("persona", "neutral")

        if not post_id:
            raise ValueError("missing post_id in message")

        # fetch post text as context (optional)
        try:
            r = requests.get(f"{BACKEND_URL}/posts/{post_id}", timeout=10)
            if r.status_code == 200:
                post_data = r.json()
                context = post_data.get("text", "")
            else:
                context = ""
        except Exception:
            context = ""

        print(f"[consumer] Generating comment for post={post_id} persona={persona}")
        text = text_gen.generate_text(additional_prompt=context, persona=persona)

        payload = {"user": user, "text": text}
        resp = requests.post(f"{BACKEND_URL}/posts/{post_id}/comments", json=payload, timeout=30)
        resp.raise_for_status()

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("[consumer] Comment created via backend")
    except Exception as e:
        print("[consumer] Error processing comment job:", e)
        traceback.print_exc()
        try:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception:
            pass


def main():
    # wait for rabbitmq to be ready a bit
    for i in range(10):
        try:
            conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
            conn.close()
            break
        except Exception:
            print("[consumer] waiting for rabbitmq...")
            time.sleep(1)

    conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    ch = conn.channel()
    ch.queue_declare(queue=QUEUE_POSTS, durable=True)
    ch.queue_declare(queue=QUEUE_COMMENTS, durable=True)
    ch.basic_qos(prefetch_count=1)

    ch.basic_consume(queue=QUEUE_POSTS, on_message_callback=process_post)
    ch.basic_consume(queue=QUEUE_COMMENTS, on_message_callback=process_comment)

    print("[consumer] Started consuming")
    ch.start_consuming()


if __name__ == "__main__":
    main()
