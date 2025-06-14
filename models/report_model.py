from pydantic import BaseModel
from typing import Optional

class Report(BaseModel):
    user_id: str
    title: str
    description: Optional[str]
    start_date: str
    end_date: str
    total_budget: float
    total_expense: float
    total_income: float
    generated_at: Optional[str] = None
