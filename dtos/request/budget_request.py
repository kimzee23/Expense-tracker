from datetime import datetime

from pydantic import BaseModel


class BudgetCreateRequest(BaseModel):
    amount: float
    start_date: datetime
    end_date: datetime
    user_id: str
class BudgetUpdateRequest(BaseModel):
    amount: float
    start_date: datetime
    end_date: datetime