from pydantic import BaseModel


class GenreCreate(BaseModel):
    genre_name: str


class GenreModel(GenreCreate):
    genre_id: int
