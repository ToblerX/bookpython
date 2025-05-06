from pydantic import BaseModel
from typing import Literal, Optional, List
from fastapi import Query
from .genre_schemas import GenreCreate


class Pagination(BaseModel):
    skip: int = 0
    limit: int = 10


sort_by_modes = ["book_name", "book_author", "book_price"]


class SortingBooks:
    def __init__(
        self,
        sort_by: Literal[*sort_by_modes] = Query(default="book_name"),
        order: Literal["asc", "desc"] = Query(default="asc"),
        genres: Optional[List[str]] = Query(default=None),
    ):
        self.sort_by = sort_by or "created_at"
        self.order = order or "asc"
        self.genres = [GenreCreate(name=genre) for genre in genres] if genres else []
