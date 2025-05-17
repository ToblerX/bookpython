from pydantic import BaseModel, validator
from app import errors, config
import re


class GenreCreate(BaseModel):
    genre_name: str

    @validator("genre_name")
    def validate_genre_name(cls, value):
        if len(value) < config.GENRE_NAME_MIN or len(value) > config.GENRE_NAME_MAX:
            raise errors.IncorrectGenreLength()
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise errors.IncorrectGenreName()
        return value


class GenreModel(GenreCreate):
    genre_id: int
