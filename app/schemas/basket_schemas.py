from pydantic import BaseModel
from typing import Optional


class BasketBase(BaseModel):
    quantity: int


class BasketCreate(BasketBase):
    book_id: int
    user_id: int


class BasketUpdate(BaseModel):
    quantity: Optional[int] = None


class BookInBasket(BaseModel):
    book_id: int
    book_name: str
    book_author: str
    book_price: float

    class Config:
        orm_mode = True


class BasketItemOut(BaseModel):
    user_id: int
    book: BookInBasket
    quantity: int

    class Config:
        orm_mode = True


class BasketItemDB(BasketBase):
    user_id: int
    book_id: int

    class Config:
        orm_mode = True
