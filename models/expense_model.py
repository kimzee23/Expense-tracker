from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Expense(BaseModel):
    id:Optional[int]
    title:str
    amount:float
    category:str
    date : datetime
    description:Optional[str] = None
    user_id:str
