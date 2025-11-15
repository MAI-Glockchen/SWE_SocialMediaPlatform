from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    image: str
    text: str
    user: str


class PostRead(BaseModel):
    id: int
    image: str
    text: str
    user: str
    created_at: datetime

    model_config = {"from_attributes": True}


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
