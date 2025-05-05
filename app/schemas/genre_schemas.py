from pydantic import BaseModel


class GenreCreate(BaseModel):
    name: str


class GenreModel(GenreCreate):
    genre_id: int
