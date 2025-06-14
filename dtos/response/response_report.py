from datetime import datetime

from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: str
    user_id: str
    total_income: float
    total_expense: float
    balance: float
    ganerate_at: datetime