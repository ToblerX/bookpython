from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from . import BookCreateId


class OrderItemCreate(BaseModel):
    book_id: int
    quantity: int


class OrderItemRead(BaseModel):
    book: BookCreateId
    quantity: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    delivery_method: str
    status: str = "pending"
    total_cost: float = Field(..., ge=0)


class OrderCreate(OrderBase):
    user_id: int
    items: List[OrderItemCreate]


class OrderRead(OrderBase):
    order_id: int
    user_id: int
    items: List[OrderItemRead]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OrderUpdateStatus(BaseModel):
    status: str
