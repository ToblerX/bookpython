import datetime
from pydantic import BaseModel, field_validator
from typing import Optional, List
from .genre_schemas import GenreCreate

from .. import errors, config


class BookModel(BaseModel):
    book_id: int
    book_name: str
    book_author: str
    book_description: str
    book_price: float
    supply: int
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
    supply: Optional[int] = None

    @field_validator("book_name")
    def validate_book_name(cls, value):
        if value is not None and (
            len(value) < config.BOOK_NAME_MIN or len(value) > config.BOOK_NAME_MAX
        ):
            raise errors.IncorrectBookNameLength()
        return value

    @field_validator("book_description")
    def validate_book_description(cls, value):
        if value is not None and (
            len(value) < config.BOOK_DESC_MIN or len(value) > config.BOOK_DESC_MAX
        ):
            raise errors.IncorrectBookDescriptionLength()
        return value

    @field_validator("book_price")
    def validate_price(cls, value):
        if value is not None and (value < 0):
            raise errors.InvalidBookPrice()
        return value

    @field_validator("supply")
    def validate_supply(cls, value):
        if value is not None and (value < 0):
            raise errors.InvalidBookSupply()
        return value


class BookCreate(BookBase):
    book_name: str
    book_author: str
    book_description: str
    book_price: float
    supply: int = 0


class BookCreateId(BookCreate):
    book_id: int


class BookUpdate(BookBase):
    pass


class BookOut(BaseModel):
    book_id: int
