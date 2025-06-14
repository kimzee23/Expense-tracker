from xml.dom.minidom import Document

from dtos.response.budget_response import BudgetResponse
from models.budget_model import Budget
from models.budget_model import Budget

def document_to_budget_model(doc) -> Budget:
    return Budget(
        id=str(doc["_id"]),
        user_id=doc["user_id"],
        amount=doc["amount"],
        start_date=doc["start_date"],
        end_date=doc["end_date"]
    )

def budget_model_to_response_dto(model: Budget):
    return {
        "id": model.id,
        "user_id": model.user_id,
        "amount": model.amount,
        "start_date": model.start_date,
        "end_date": model.end_date
    }