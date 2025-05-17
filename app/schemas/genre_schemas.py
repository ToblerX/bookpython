from pydantic import BaseModel, validator
from app import errors
import re


class GenreCreate(BaseModel):
    genre_name: str

    @validator("genre_name")
    def validate_genre_name(cls, value):
        if len(value) < 3 or len(value) > 30:
            raise errors.IncorrectGenreLength()
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise errors.IncorrectGenreName()
        return value


class GenreModel(GenreCreate):
    genre_id: int
