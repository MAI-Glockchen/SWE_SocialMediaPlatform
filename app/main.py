from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlmodel import select

from .database import get_session, init_db
from .models import Comment, Post
from .schemas import CommentCreate, CommentRead, PostCreate, PostRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Simple Social API", lifespan=lifespan)


@app.post("/posts/", response_model=PostRead)
def create_post(post: PostCreate):
    with get_session() as session:
        new_post = Post(**post.model_dump())
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return PostRead.from_orm(new_post)


@app.get("/posts/", response_model=list[PostRead])
def get_all_posts():
    with get_session() as session:
        query = select(Post).order_by(Post.created_at.desc())
        posts = session.exec(query).all()

        if not posts:
            raise HTTPException(404, "No posts found")

        return [PostRead.from_orm(post) for post in posts]  # <- fix


@app.get("/posts/{post_id}", response_model=PostRead)
def get_post_by_id(post_id: int):
    with get_session() as session:
        post = session.exec(select(Post).where(Post.id == post_id)).first()

        if not post:
            raise HTTPException(404, "Post not found")

        return PostRead.from_orm(post)


@app.get("/posts/{post_id}/comments", response_model=list[CommentRead])
def get_comments_for_post_id(post_id: int):
    with get_session() as session:
        comments = session.exec(
            select(Comment).where(Comment.super_id == post_id)
        ).all()

        if not comments:
            raise HTTPException(404, "No comments found for this post")

        return comments


@app.post("/posts/{post_id}/comments", response_model=CommentRead)
def create_comment_for_post(post_id: int, comment: CommentCreate):
    with get_session() as session:
        new_comment = Comment(super_id=post_id, **comment.model_dump())
        session.add(new_comment)
        session.commit()
        session.refresh(new_comment)
        return CommentRead.from_orm(new_comment)
