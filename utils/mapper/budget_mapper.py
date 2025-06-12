from xml.dom.minidom import Document

from dtos.response.budget_response import BudgetResponse
from models.budget_model import Budget


def document_to_budget_model(document: Document) -> Budget:
    return Budget(
        id = str(document["_id"]),
        amount=float(document["amount"]),
        start_date=document["start_date"],
        end_date=document["end_date"],
        user_id=str(document["user_id"]),
    )
def budget_model_to_response_dto(model: Budget) -> BudgetResponse:
    return BudgetResponse(
        id = str(model.id),
        amount=model.amount,
        start_date=model.start_date,
        end_date=model.end_date,
        user_id=model.user_id
    )