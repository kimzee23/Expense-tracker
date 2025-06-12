from datetime import datetime

from pydantic import BaseModel


class Budget(BaseModel):
    amount: float
    start_date: datetime
    end_date: datetime
    user_id: str