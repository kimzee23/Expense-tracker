from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Expense(BaseModel):
    id: Optional[str] = None
    title: str
    amount: float
    category: str
    date: datetime
    description: Optional[str] = None
    user_id: str
