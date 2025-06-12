
from datetime import datetime

from pydantic import BaseModel, Field


class ExpenseCreateRequest(BaseModel):
    title: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    date: datetime
    description: str
    user_id: str = Field(min_length=1)

class ExpenseUpdateRequest(BaseModel):
    title: str | None = None
    amount: float | None = None
    category: str | None = None
    date: datetime | None = None
