from models.expense_model import Expense
from dtos.response.expense_response import ExpenseResponse

def expense_model_to_response_dto(expense: Expense) -> ExpenseResponse:
    return ExpenseResponse(
        id=str(expense.id),
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        date=expense.date,
        user_id=expense.user_id
    )

def document_to_expense_model(doc: dict) -> Expense:
    return Expense(
        id=str(doc.get("_id")),
        title=doc.get("title"),
        amount=doc.get("amount"),
        category=doc.get("category"),
        date=doc.get("date"),
        description=doc.get("description"),
        user_id=str(doc.get("user_id"))
    )
