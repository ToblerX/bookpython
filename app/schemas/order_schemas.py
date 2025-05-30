from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class OrderItemSchema(BaseModel):
    book_id: int
    quantity: int = Field(..., gt=0)


class OrderBase(BaseModel):
    delivery_method: str
    status: str = "pending"
    total_cost: float = Field(..., ge=0)


class OrderCreate(OrderBase):
    user_id: int
    items: List[OrderItemSchema]


class OrderRead(OrderBase):
    order_id: int
    user_id: int
    items: List[OrderItemSchema]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OrderUpdateStatus(BaseModel):
    status: str
