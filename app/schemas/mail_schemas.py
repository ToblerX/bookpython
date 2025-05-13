from typing import List
from pydantic import BaseModel, EmailStr


class EmailModel(BaseModel):
    addresses: List[EmailStr]
