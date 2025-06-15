from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Report(BaseModel):
    user_id: str
    title: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime
    total_budget: float
    total_expense: float
    total_income: float
    generated_at: Optional[datetime] = None
