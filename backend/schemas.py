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
    def from_orm_bytes(cls, obj):
        return cls(
            id=obj.id,
            text=obj.text,
            user=obj.user,
            created_at=obj.created_at,
            image=(
                base64.b64encode(obj.image).decode()
                if obj.image else None
            )
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

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        """
        Pydantic v2 style ORM conversion.
        """
        return cls.model_validate(obj, from_attributes=True)
