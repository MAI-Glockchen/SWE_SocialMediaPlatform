from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    image_full: Optional[bytes] = None
    image_thumb: Optional[bytes] = None
    text: str
    user: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
