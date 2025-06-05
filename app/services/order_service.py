import time

from pydantic import EmailStr
from sqlalchemy.orm import Session, selectinload

from .. import config, mail
from ..exceptions import errors
from ..db import models
from ..db.models import Order, Book
from ..schemas import OrderCreate, OrderItemRead
from sqlalchemy import insert


def create_order(order_data: OrderCreate, current_session: Session):
    # Calculate total cost and check stock availability
    total = 0
    book_ids = [item.book_id for item in order_data.items]
    books = current_session.query(Book).filter(Book.book_id.in_(book_ids)).all()

    book_map = {book.book_id: book for book in books}
    for item in order_data.items:
        book = book_map.get(item.book_id)
        if not book:
            raise errors.BookNotFound

        if book.supply < item.quantity:
            raise errors.SupplyTooSmall

        total += book.book_price * item.quantity

    try:
        # Create the Order
        order = Order(
            user_id=order_data.user_id,
            delivery_method=order_data.delivery_method,
            total_cost=total,
            status=order_data.status,
        )
        current_session.add(order)
        current_session.flush()  # flush to get order.order_id without committing

        # Insert items into association table
        current_session.execute(
            insert(models.OrderItem),
            [
                {
                    "order_id": order.order_id,
                    "book_id": item.book_id,
                    "quantity": item.quantity,
                }
                for item in order_data.items
            ],
        )

        # Subtract supply for each book
        for item in order_data.items:
            book = book_map[item.book_id]
            book.supply -= item.quantity
            current_session.add(book)  # mark book as dirty for update

        current_session.commit()
        current_session.refresh(order)

    except Exception as e:
        current_session.rollback()
        raise e

    return order


def get_order(order_id: int, current_session: Session):
    return current_session.query(Order).filter(Order.order_id == order_id).first()


def get_user_orders(user_id: int, current_session: Session):
    return (
        current_session.query(Order)
        .options(selectinload(Order.order_items).selectinload(models.OrderItem.book))
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )


def set_order_status(order_id: int, status: str, current_session: Session):
    order = current_session.query(Order).filter(Order.order_id == order_id).first()
    order.status = status
    current_session.commit()
    current_session.refresh(order)
    return order


async def send_order_information_email(
    user_email: EmailStr, order_id: int, total_cost: float, items: list[OrderItemRead]
):
    items_str = ""
    for item in items:
        item_link = f"http://{config.DOMAIN}/books/{item.book.book_id}"
        cover_url = f"http://{config.DOMAIN}/books/{item.book.book_id}/cover?ts={int(time.time())}"
        items_str += f"""
        <div style="margin-bottom: 15px;">
            <a href="{item_link}" style="text-decoration: none; color: inherit;">
                <img src="{cover_url}" width="100" style="display: block; border: 1px solid #ccc; margin-bottom: 5px;" />
                <strong>{item.book.book_name} x {item.quantity} x {item.book.book_price}$</strong>
            </a>
        </div>
        """

    html_message = f"""
            <h1>Your order has been placed successfully!</h1>
            <p>Thank you for choosing bookpython!</p>
            <p>Order id: {order_id}</p>
            <p>Total cost: {total_cost}$</p>
            <h3>The list of items:</h3>
            {items_str}
            """

    message = mail.create_message(
        recipients=[user_email],
        subject="New Order",
        body=html_message,
    )

    await mail.mail_engine.send_message(message)

    return {"status": "Email sent successfully"}
