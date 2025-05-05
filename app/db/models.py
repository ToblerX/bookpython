import datetime
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey, Float
from sqlalchemy.orm import relationship
from . import database

# Association table for many-to-many relationship between books and genres
# book_genres = Table(
#    "book_genres",
#    database.Base.metadata,
#    Column("book_id", Integer, ForeignKey("books.book_id"), primary_key=True),
#    Column("genre_id", Integer, ForeignKey("genres.genre_id"), primary_key=True),
# )


class User(database.Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


class Book(database.Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    book_name = Column(String, nullable=False, unique=True)
    book_author = Column(String, nullable=False)
    book_description = Column(String, nullable=False)
    # price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


#    genres = relationship("Genre", secondary=book_genres)


class Genre(database.Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
