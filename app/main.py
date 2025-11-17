import base64
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session, init_db
from app.models import Comment, Post
from app.schemas import CommentCreate, CommentRead, PostCreate, PostRead


# -----------------------
# Dependency for FastAPI
# -----------------------
def get_session_dep():
    """FastAPI dependency that yields a SQLModel Session."""
    with get_session() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Simple Social API", lifespan=lifespan)


@app.post("/posts/", response_model=PostRead)
def create_post(post: PostCreate, session: Session = Depends(get_session_dep)):
    # Decode Base64 string (tests pass plain strings but still valid)

    try:
        image_bytes = base64.b64decode(post.image)
    except Exception:
        raise HTTPException(400, "Invalid base64 image string")

    new_post = Post(image=image_bytes, text=post.text, user=post.user)

    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    # Encode bytes → base64 for output
    return PostRead.from_orm_bytes(new_post)


@app.get("/posts/", response_model=list[PostRead])
def get_all_posts(
    text: str = Query(None, description="Search term for text"),
    user: str = Query(None, description="Filter by author username"),
    session: Session = Depends(get_session_dep),
):
    query = select(Post)

    if text:
        query = query.where(Post.text.ilike(f"%{text}%"))
    if user:
        query = query.where(Post.user == user)

    query = query.order_by(Post.created_at.desc())
    posts = session.exec(query).all()

    if not posts:
        raise HTTPException(404, "No posts found")

    return [PostRead.from_orm_bytes(post) for post in posts]


@app.get("/posts/{post_id}", response_model=PostRead)
def get_post_by_id(post_id: int, session: Session = Depends(get_session_dep)):
    post = session.exec(select(Post).where(Post.id == post_id)).first()

    if not post:
        raise HTTPException(404, "Post not found")

    return PostRead.from_orm_bytes(post)


@app.get("/posts/{post_id}/comments", response_model=list[CommentRead])
def get_comments_for_post_id(
    post_id: int,
    text: str = Query(None, description="Search term in comment text"),
    user: str = Query(None, description="Filter by comment user"),
    session: Session = Depends(get_session_dep),
):
    query = select(Comment).where(Comment.super_id == post_id)

    if text:
        query = query.where(Comment.text.ilike(f"%{text}%"))
    if user:
        query = query.where(Comment.user == user)

    comments = session.exec(query).all()

    if not comments:
        raise HTTPException(404, "No comments found for this post")

    return [CommentRead.from_orm(comment) for comment in comments]


@app.get("/comments/{comment_id}", response_model=CommentRead)
def get_comment_by_id(comment_id: int, session: Session = Depends(get_session_dep)):
    comment = session.exec(
        select(Comment).where(Comment.comment_id == comment_id)
    ).first()

    if not comment:
        raise HTTPException(404, "Comment not found")

    return CommentRead.from_orm(comment)


@app.post("/posts/{post_id}/comments", response_model=CommentRead)
def create_comment_for_post(
    post_id: int,
    comment: CommentCreate,
    session: Session = Depends(get_session_dep),
):
    new_comment = Comment(super_id=post_id, **comment.model_dump())

    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)

    return CommentRead.from_orm(new_comment)
