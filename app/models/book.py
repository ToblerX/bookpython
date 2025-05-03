import datetime
from pydantic import BaseModel

class BookModel(BaseModel):
    id: int
    name: str
    author: str
    description: str
    created_at: datetime
    updated_at: datetime