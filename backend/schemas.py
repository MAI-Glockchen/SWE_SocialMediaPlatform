import base64
from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    image: str | None = None
    text: str
    user: str

    def to_model_bytes(self) -> bytes:
        return base64.b64decode(self.image.encode())


class PostRead(BaseModel):
    id: int
    image: str | None = None  # API returns Base64 string
    text: str
    user: str
    created_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_bytes(cls, obj):
        return cls(
            id=obj.id,
            image=base64.b64encode(obj.image).decode(),
            text=obj.text,
            user=obj.user,
            created_at=obj.created_at,
        )


class CommentCreate(BaseModel):
    text: str
    user: str


class CommentRead(BaseModel):
    super_id: int
    comment_id: int
    text: str
    user: str
    created_at: datetime

    model_config = {"from_attributes": True}
