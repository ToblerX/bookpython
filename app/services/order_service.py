from typing import List

from sqlalchemy.orm import Session
from ..db.models import Order, Book, order_items
from ..schemas import OrderCreate, OrderItemSchema
from sqlalchemy import insert


def create_order(db: Session, order_data: OrderCreate):
    # Calculate total cost
    total = 0
    book_ids = [item.book_id for item in order_data.items]
    books = db.query(Book).filter(Book.book_id.in_(book_ids)).all()

    book_map = {book.book_id: book for book in books}
    for item in order_data.items:
        book = book_map.get(item.book_id)
        if not book:
            raise ValueError(f"Book ID {item.book_id} not found.")
        total += book.book_price * item.quantity

    # Create the Order
    order = Order(
        user_id=order_data.user_id,
        delivery_method=order_data.delivery_method,
        total_cost=total,
        status=order_data.status,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Insert items into the association table
    db.execute(
        insert(order_items),
        [
            {
                "order_id": order.order_id,
                "book_id": item.book_id,
                "quantity": item.quantity,
            }
            for item in order_data.items
        ],
    )
    db.commit()

    return order


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.order_id == order_id).first()


def get_user_orders(db: Session, user_id: int) -> List[Order]:
    return (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )
