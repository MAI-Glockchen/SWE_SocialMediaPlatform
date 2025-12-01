import base64
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

class PostCreate(BaseModel):
    image: Optional[str] = None    # base64 or data URL
    text: str
    user: str

class PostRead(BaseModel):
    id: int
    image: Optional[str] = None      # base64 string for frontend
    text: str
    user: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_bytes(cls, post):
        """
        Convert a SQLModel Post (with bytes) into a Pydantic model where
        image is base64 encoded for the Angular frontend.
        """
        # Convert bytes → base64 string
        encoded = base64.b64encode(post.image).decode("utf-8") if post.image else None

        # Validate object using Pydantic v2 API
        model = cls.model_validate(post, from_attributes=True)

        # Override image with encoded version
        return model.model_copy(update={"image": encoded})

class CommentCreate(BaseModel):
    text: str
    user: str
    
class CommentRead(BaseModel):
    super_id: int
    comment_id: int
    text: str
    user: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        """
        Pydantic v2 style ORM conversion.
        """
        return cls.model_validate(obj, from_attributes=True)
