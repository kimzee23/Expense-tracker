from datetime import datetime

from pydantic import BaseModel


class ExpenseResponse(BaseModel):
    id:str
    amount:float
    category:str
    date:datetime
    description:str
    user_id:str