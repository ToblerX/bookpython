import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Table,
    ForeignKey,
    Float,
    Boolean,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from . import database

# Association table for many-to-many relationship between books and genres
book_genres = Table(
    "book_genres",
    database.Base.metadata,
    Column("book_id", Integer, ForeignKey("books.book_id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.genre_id"), primary_key=True),
)

# Association table for many-to-many relationship between books and users (wishlist)
user_books_wishlist = Table(
    "user_books",
    database.Base.metadata,
    Column("book_id", Integer, ForeignKey("books.book_id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
)


class User(database.Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    verified = Column(Boolean, default=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    wishlist = relationship("Book", secondary=user_books_wishlist)
    basket_items = relationship(
        "BasketItem", back_populates="user", cascade="all, delete-orphan"
    )


class Book(database.Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    book_name = Column(String, nullable=False, unique=True)
    book_author = Column(String, nullable=False)
    book_description = Column(String, nullable=False)
    book_price = Column(Float, nullable=False)
    supply = Column(Integer, default=0)
    book_cover_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    __table_args__ = (CheckConstraint("supply >= 0", name="check_supply_non_negative"),)

    genres = relationship("Genre", secondary=book_genres)
    basket_items = relationship("BasketItem", back_populates="book")


class Genre(database.Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    genre_name = Column(String, nullable=False, unique=True)


class BasketItem(database.Base):
    __tablename__ = "baskets"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("books.book_id"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)

    user = relationship("User", back_populates="basket_items")
    book = relationship("Book", back_populates="basket_items")
