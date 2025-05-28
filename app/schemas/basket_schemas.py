from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


class BasketItemOut(BaseModel):
    user_id: int
    book: BookInBasket
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class BasketItemDB(BasketBase):
    user_id: int
    book_id: int

    class Config:
        orm_mode = True
