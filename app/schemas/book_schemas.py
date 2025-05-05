import datetime
from pydantic import BaseModel
from typing import Optional, List


class BookModel(BaseModel):
    book_id: int
    book_name: str
    book_author: str
    book_description: str
    book_price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class BookGenresIds(BookModel):
    genres_ids: Optional[List[int]] = None


class BookGenresNames(BookModel):
    genres_ids: Optional[List[str]] = None


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
