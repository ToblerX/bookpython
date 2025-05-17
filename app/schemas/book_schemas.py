import datetime
from pydantic import BaseModel, validator
from typing import Optional, List
from .genre_schemas import GenreCreate

from .. import errors, config


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


class BookBase(BaseModel):
    book_name: Optional[str] = None
    book_author: Optional[str] = None
    book_description: Optional[str] = None
    book_price: Optional[float] = None

    @validator("book_name")
    def validate_book_name(cls, value):
        if value is not None and (
            len(value) < config.BOOK_NAME_MIN or len(value) > config.BOOK_NAME_MAX
        ):
            raise errors.IncorrectBookNameLength()
        return value

    @validator("book_description")
    def validate_book_description(cls, value):
        if value is not None and (
            len(value) < config.BOOK_DESC_MIN or len(value) > config.BOOK_DESC_MAX
        ):
            raise errors.IncorrectBookDescriptionLength()
        return value


class BookCreate(BookBase):
    book_name: str
    book_author: str
    book_description: str
    book_price: float


class BookUpdate(BookBase):
    pass
