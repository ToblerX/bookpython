import datetime
from pydantic import BaseModel
from typing import Optional


class BookModel(BaseModel):
    book_id: int
    book_name: str
    book_author: str
    book_description: str
    # book_price: float
    created_at: datetime
    updated_at: datetime
    # genres: Optional[list[int]] = None

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class BookCreate(BaseModel):
    book_name: str
    book_author: str
    book_description: str
    # book_price: float


class BookId(BaseModel):
    book_id: int


class BookUpdate(BookId):
    book_name: Optional[str] = None
    book_author: Optional[str] = None
    book_description: Optional[str] = None
    # book_price: Optional[float] = None
