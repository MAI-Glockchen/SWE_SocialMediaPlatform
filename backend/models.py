from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    image: Optional[bytes] = None  # store image as blob
    text: str
    user: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


class Comment(SQLModel, table=True):
    super_id: int | None = Field(default=None, foreign_key="post.id")
    comment_id: int | None = Field(default=None, primary_key=True)
    text: str
    user: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )