

from pydantic import BaseModel
from datetime import date
from typing import Optional

class Budget(BaseModel):
    id: Optional[str] = None
    user_id: str
    amount: float
    start_date: date
    end_date: date
