import datetime
from pydantic import BaseModel
from typing import Optional, List
from .genre_schemas import GenreCreate


class BookModel(BaseModel):
    book_id: int
    book_name: str
    book_author: str
    book_description: str
    book_price: float
    book_cover_path: str
    genres: Optional[List[GenreCreate]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class BookCreate(BaseModel):
    book_name: str
    book_author: str
    book_description: str
    book_price: float


class BookUpdate(BaseModel):
    book_name: Optional[str] = None
    book_author: Optional[str] = None
    book_description: Optional[str] = None
    book_price: Optional[float] = None
