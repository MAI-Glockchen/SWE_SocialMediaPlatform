import io
import json
import time
import pika

from pika.exceptions import AMQPError
from PIL import Image
from sqlmodel import Session, create_engine, select

from models import Post

RABBIT_HOST = "rabbitmq"
QUEUE = "image.resize"
DB_URL = "sqlite:///sqlite/social.db"

engine = create_engine(DB_URL, echo=False)


def process_message(ch, method, properties, body):
    payload = json.loads(body)
    post_id: int = payload["post_id"]

    with Session(engine) as session:
        post = session.exec(select(Post).where(Post.id == post_id)).first()

        if post is None or post.image_full is None:
            return

        img = Image.open(io.BytesIO(post.image_full))
        img.thumbnail((400, 400))

        buf = io.BytesIO()
        img.save(buf, format="PNG")

        post.image_thumb = buf.getvalue()
        session.add(post)
        session.commit()


def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_consume(
        queue=QUEUE,
        on_message_callback=process_message,
        auto_ack=True,
    )

    print("[image-resizer] waiting for resize jobs")
    channel.start_consuming()


def main():
    original_delay = 0.5
    retry_delay = original_delay
    while True:
        try:
            consume()
            retry_delay = original_delay
        except AMQPError as e:
            print(f"[image-resizer] connection lost: {e}, retrying in {retry_delay} seconds.")
            time.sleep(retry_delay)
            retry_delay = retry_delay * 2 - original_delay / 2
            if retry_delay > 60:
                print("[image-resizer] giving up on connection retry. Abort service.")
                break


if __name__ == "__main__":
    main()
