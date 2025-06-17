from typing import List
from dtos.request.expense_request import ExpenseCreateRequest, ExpenseUpdateRequest
from dtos.response.expense_response import ExpenseResponse
from models.expense_model import Expense
from repositories.expanse_repository import ExpenseRepository
from utils.mapper.expense_mapper import expense_model_to_response_dto, document_to_expense_model
from exceptions.expense_exception import ExpenseNotFound

class ExpenseService:
    def __init__(self, repo: ExpenseRepository):
        self.repo = repo

    def create_expense(self, request_dto: ExpenseCreateRequest) -> str:
        expense = Expense(
            title=request_dto.title.strip(),
            amount=request_dto.amount,
            category=request_dto.category.strip(),
            date=request_dto.date,
            description=request_dto.description,
            user_id=request_dto.user_id.strip()
        )
        return self.repo.create_expense(expense.dict())

    def get_expenses(self, user_id: str) -> list[ExpenseResponse]:
        documents = self.repo.get_expense_by_user_id(user_id)
        return [
            expense_model_to_response_dto(document_to_expense_model(doc))
            for doc in documents
        ]

    def get_expense_by_id(self, expense_id: str) -> ExpenseResponse:
        doc = self.repo.get_expense_by_id(expense_id)
        if not doc:
            raise ExpenseNotFound("Expense not found")
        model = document_to_expense_model(doc)
        return expense_model_to_response_dto(model)

    def update_expense(self, expense_id: str, request_dto: ExpenseUpdateRequest) -> bool:
        update_data = {
            key: value for key, value in request_dto.model_dump().items()
            if value is not None
        }
        if not update_data:
            return False
        success = self.repo.update_expense(expense_id, update_data)
        if not success:
            raise ExpenseNotFound("Expense not found or not updated")
        return True

    def delete_expense(self, expense_id: str) -> bool:
        success = self.repo.delete_expense(expense_id)
        if not success:
            raise ExpenseNotFound("Expense not found or already deleted")
        return True
