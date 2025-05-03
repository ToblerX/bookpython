import datetime
from pydantic import BaseModel


class BookModel(BaseModel):
    id: int
    name: str
    author: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class BookCreate(BaseModel):
    name: str
    author: str
    description: str


class BookId(BaseModel):
    id: int
