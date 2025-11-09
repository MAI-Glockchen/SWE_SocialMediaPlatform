from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from sqlmodel import select
from .database import get_session, init_db
from .models import Post
from .schemas import PostCreate, PostRead
# Testcommit
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
        return new_post

@app.get("/posts/last", response_model=PostRead)
def get_last_post():
    with get_session() as session:
        result = session.exec(select(Post).order_by(Post.created_at.desc())).first()
        if not result:
            raise HTTPException(404, "No posts found")
        return result
