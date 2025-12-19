import base64
import json
import os
import re
from contextlib import asynccontextmanager

import pika
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from backend.database import get_session, init_db
from backend.models import Comment, Post
from backend.schemas import (
    CommentCreate,
    CommentRead,
    GeneratedCommentCreate,
    GeneratedPostCreate,
    PostCreate,
    PostRead,
)
from post_generator.generator import TextGenerator

TESTING = os.environ.get("WALLOH_SOCIAL_TESTING") == "1"

ai_generator = TextGenerator()


# -------------------------------------------------
# RabbitMQ helper
# -------------------------------------------------
def publish_resize_job(post_id: int) -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="image.resize", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="image.resize",
        body=json.dumps({"post_id": post_id}),
    )

    connection.close()


# -------------------------------------------------
# FastAPI setup
# -------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Simple Social API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# Create Post (publish resize job)
# -------------------------------------------------
@app.post("/posts/", response_model=PostRead)
def create_post(post: PostCreate, session: Session = Depends(get_session)):
    raw = post.image
    if raw is None or raw.strip() == "":
        image_bytes = None
    elif raw.startswith("/assets/"):
        image_bytes = None
    else:
        raw = raw.strip()
        if raw.startswith("data:"):
            match = re.match(r"data:.*?;base64,(.*)", raw, re.DOTALL)
            if not match:
                raise HTTPException(400, "Invalid data URL format")
            raw = match.group(1)
        raw = raw.replace("\n", "").replace("\r", "").replace(" ", "")
        try:
            image_bytes = base64.b64decode(raw, validate=False)
        except Exception:
            raise HTTPException(400, "Invalid base64 image string")

    new_post = Post(
        image_full=image_bytes,
        image_thumb=None,
        text=post.text,
        user=post.user,
    )

    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    if not TESTING and new_post.image_full is not None and new_post.id is not None:
        publish_resize_job(new_post.id)

    return PostRead.from_orm_bytes(new_post)


@app.post("/posts/generate", response_model=PostRead)
def create_post_with_ai(post: GeneratedPostCreate, session: Session = Depends(get_session)):
    """
    Generate a post using AI based on the prompt and persona,
    then save it to the database.
    """
    generated_text = ai_generator.generate_text(additional_prompt=post.prompt, persona=post.persona)
    new_post_data = PostCreate(text=generated_text, user=post.user, image=post.image)
    new_post = create_post(new_post_data, session=session)
    return new_post


@app.post("/posts/{post_id}/comments/generate", response_model=CommentRead)
def create_comment_with_ai(
    post_id: int,
    comment: GeneratedCommentCreate,
    session: Session = Depends(get_session),
):
    post = session.exec(select(Post).where(Post.id == post_id)).first()
    if not post:
        raise HTTPException(404, "Post not found")

    generated_text = ai_generator.generate_text(
        additional_prompt=post.text,
        persona=comment.persona,
    )

    new_comment = Comment(
        super_id=post_id,
        text=generated_text,
        user=comment.user,
    )

    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)

    return CommentRead.from_orm(new_comment)


# -------------------------------------------------
# Get all posts (list view → thumbnails later)
# -------------------------------------------------
@app.get("/posts/", response_model=list[PostRead])
def get_all_posts(
    text: str | None = Query(None, description="Search term for text"),
    user: str | None = Query(None, description="Filter by author username"),
    session: Session = Depends(get_session),
):
    query = select(Post)
    if text:
        # The comment in the next row is necessary to silence Pylance
        query = query.where(Post.text.ilike(f"%{text}%"))  # type: ignore[attr-defined]
    if user:
        query = query.where(Post.user == user)
    # The comment in the next row is necessary to silence Pylance
    query = query.order_by(Post.created_at.desc())  # type: ignore[attr-defined]

    posts = session.exec(query).all()
    if not posts:
        raise HTTPException(404, "No posts found")
    return [PostRead.from_orm_bytes(post) for post in posts]


# -------------------------------------------------
# Get single post (detail view → full image later)
# -------------------------------------------------
@app.get("/posts/{post_id}", response_model=PostRead)
def get_post_by_id(post_id: int, session: Session = Depends(get_session)):
    post = session.exec(select(Post).where(Post.id == post_id)).first()
    if not post:
        raise HTTPException(404, "Post not found")
    return PostRead.from_orm_bytes(post)


# -----------------------------------------------------------
# Delete Post (and its comments)
# -----------------------------------------------------------
@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, session: Session = Depends(get_session)):
    post = session.exec(select(Post).where(Post.id == post_id)).first()
    if not post:
        raise HTTPException(404, "Post not found")

    comments = session.exec(select(Comment).where(Comment.super_id == post_id)).all()
    for c in comments:
        session.delete(c)

    session.delete(post)
    session.commit()
    return None


# -----------------------------------------------------------
# Get comments for a post
# -----------------------------------------------------------
@app.get("/posts/{post_id}/comments", response_model=list[CommentRead])
def get_comments_for_post(
    post_id: int,
    text: str | None = Query(None, description="Search term in comment text"),
    user: str | None = Query(None, description="Filter by comment user"),
    session: Session = Depends(get_session),
):
    query = select(Comment).where(Comment.super_id == post_id)
    if text:
        query = query.where(Comment.text.ilike(f"%{text}%"))  # type: ignore[attr-defined]
    if user:
        query = query.where(Comment.user == user)

    comments = session.exec(query).all()
    return [CommentRead.from_orm(c) for c in comments]


@app.post("/posts/{post_id}/comments", response_model=CommentRead)
def create_comment(post_id: int, comment: CommentCreate, session: Session = Depends(get_session)):
    new_comment = Comment(super_id=post_id, **comment.model_dump())
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return CommentRead.from_orm(new_comment)


@app.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int, session: Session = Depends(get_session)):
    comment = session.exec(select(Comment).where(Comment.comment_id == comment_id)).first()
    if not comment:
        raise HTTPException(404, "Comment not found")
    session.delete(comment)
    session.commit()
    return None


@app.get("/comments/{comment_id}", response_model=CommentRead)
def get_comment_by_id(comment_id: int, session: Session = Depends(get_session)):
    comment = session.exec(select(Comment).where(Comment.comment_id == comment_id)).first()
    if not comment:
        raise HTTPException(404, "Comment not found")
    return CommentRead.from_orm(comment)
