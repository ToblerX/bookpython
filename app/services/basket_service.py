from sqlalchemy.orm import Session
from .. import schemas, errors
from .. import db as app_db


def add_to_basket(user_id: int, book_id: int, quantity: int, current_session: Session):
    existing_item = (
        current_session.query(app_db.models.BasketItem)
        .filter_by(user_id=user_id, book_id=book_id)
        .first()
    )

    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = app_db.models.BasketItem(
            user_id=user_id, book_id=book_id, quantity=quantity
        )
        current_session.add(new_item)

    current_session.commit()
    return {"message": "Book added to basket."}


def get_basket(user_id: int, current_session: Session) -> list[schemas.BasketItemOut]:
    items = (
        current_session.query(app_db.models.BasketItem)
        .filter(app_db.models.BasketItem.user_id == user_id)
        .all()
    )
    return [
        schemas.BasketItemOut(
            user_id=item.user_id, quantity=item.quantity, book=item.book
        )
        for item in items
    ]


def delete_from_basket(user_id: int, book_id: int, current_session: Session):
    item = (
        current_session.query(app_db.models.BasketItem)
        .filter_by(user_id=user_id, book_id=book_id)
        .first()
    )

    if not item:
        raise errors.BookNotFoundInBasket

    current_session.delete(item)
    current_session.commit()
    return {"message": "Book removed from basket."}


def update_basket_quantity(
    user_id: int,
    book_id: int,
    update_data: schemas.BasketUpdate,
    current_session: Session,
):
    item = (
        current_session.query(app_db.models.BasketItem)
        .filter_by(user_id=user_id, book_id=book_id)
        .first()
    )

    if not item:
        raise errors.BookNotFoundInBasket

    if update_data.quantity is None or update_data.quantity < 1:
        raise errors.QuantityError

    item.quantity = update_data.quantity
    current_session.commit()
    return {"message": "Basket item updated.", "quantity": item.quantity}


def clear_basket(user_id: int, current_session: Session):
    current_session.query(app_db.models.BasketItem).filter_by(user_id=user_id).delete()
    current_session.commit()
    return {"message": "Basket cleared."}
