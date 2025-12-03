import base64
import re
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from backend.database import get_session, init_db
from backend.models import Comment, Post
from backend.schemas import CommentCreate, CommentRead, PostCreate, PostRead


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

# -----------------------
# CORS
# -----------------------
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


# -----------------------------------------------------------
# Create Post
# -----------------------------------------------------------
@app.post("/posts/", response_model=PostRead)
def create_post(post: PostCreate, session: Session = Depends(get_session_dep)):

    raw = post.image

    # 1) No image provided -> keep None
    if raw is None or raw.strip() == "":
        image_bytes = None

    # 2) Frontend default placeholder -> store None
    elif raw.startswith("/assets/"):
        image_bytes = None

    else:
        raw = raw.strip()

        # 3) Data URL
        if raw.startswith("data:"):
            match = re.match(r"data:.*?;base64,(.*)", raw, re.DOTALL)
            if not match:
                raise HTTPException(400, "Invalid data URL format")
            raw = match.group(1)

        # 4) Clean whitespace
        raw = raw.replace("\n", "").replace("\r", "").replace(" ", "")

        # 5) Decode base64
        try:
            image_bytes = base64.b64decode(raw, validate=False)
        except Exception:
            raise HTTPException(400, "Invalid base64 image string")

    new_post = Post(
        image=image_bytes,
        text=post.text,
        user=post.user
    )

    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return PostRead.from_orm_bytes(new_post)

    # =============================================
    # Create post in DB
    # =============================================
    new_post = Post(
        image=image_bytes,
        text=post.text,
        user=post.user
    )

    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    # Convert to Pydantic v2 model (base64 → string)
    return PostRead.from_orm_bytes(new_post)


# -----------------------------------------------------------
# Get all posts
# -----------------------------------------------------------
@app.get("/posts/", response_model=list[PostRead])
def get_all_posts(
    text: str | None = Query(None, description="Search term for text"),
    user: str | None = Query(None, description="Filter by author username"),
    session: Session = Depends(get_session_dep),
):
    query = select(Post)

    if text:
        # The comment in the next row is necessary to silence Pylance, because it doesnt understand SQL-Alchemy-attributes here:
        query = query.where(Post.text.ilike(f"%{text}%"))  # type: ignore[attr-defined]
    if user:
        query = query.where(Post.user == user)
    # The comment in the next row is necessary to silence Pylance, because it doesnt understand SQL-Alchemy-attributes here:
    query = query.order_by(Post.created_at.desc())  # type: ignore[attr-defined].

    posts = session.exec(query).all()

    if not posts:
        raise HTTPException(404, "No posts found")

    return [PostRead.from_orm_bytes(post) for post in posts]


# -----------------------------------------------------------
# Get Post by ID
# -----------------------------------------------------------
@app.get("/posts/{post_id}", response_model=PostRead)
def get_post_by_id(post_id: int, session: Session = Depends(get_session_dep)):
    post = session.exec(select(Post).where(Post.id == post_id)).first()

    if not post:
        raise HTTPException(404, "Post not found")

    return PostRead.from_orm_bytes(post)


# -----------------------------------------------------------
# Get comments for a post
# -----------------------------------------------------------
@app.get("/posts/{post_id}/comments", response_model=list[CommentRead])
def get_comments_for_post_id(
    post_id: int,
    text: str | None = Query(None, description="Search term in comment text"),
    user: str | None = Query(None, description="Filter by comment user"),
    session: Session = Depends(get_session_dep),
):
    query = select(Comment).where(Comment.super_id == post_id)

    if text:
        query = query.where(Comment.text.ilike(f"%{text}%"))  # type: ignore[attr-defined]
    if user:
        query = query.where(Comment.user == user)

    comments = session.exec(query).all()


    return [CommentRead.from_orm(comment) for comment in comments]


# -----------------------------------------------------------
# Get comment by ID
# -----------------------------------------------------------
@app.get("/comments/{comment_id}", response_model=CommentRead)
def get_comment_by_id(comment_id: int, session: Session = Depends(get_session_dep)):
    comment = session.exec(
        select(Comment).where(Comment.comment_id == comment_id)
    ).first()

    if not comment:
        raise HTTPException(404, "Comment not found")

    return CommentRead.from_orm(comment)


# -----------------------------------------------------------
# Create comment
# -----------------------------------------------------------
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
