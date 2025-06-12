from datetime import datetime

from pydantic import BaseModel


class BudgetResponse(BaseModel):
    id: str
    amount: float
    start_date: datetime
    end_date: datetime
    user_id: str
