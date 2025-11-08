from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    image: str
    text: str
    user: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
