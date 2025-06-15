from typing import Optional

from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    total_income: float
    total_expense: float
    total_budget: float
    balance: float
    generated_at: str
