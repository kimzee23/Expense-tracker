from exceptions.not_found_exception import NotFoundException
from repositories.budget_repository import BudgetRepository
from utils.mapper.budget_mapper import document_to_budget_model, budget_model_to_response_dto


class BudgetService:
    def __init__(self, db):
        self.budget_collection = db["budgets"]
        self.repo = BudgetRepository(db)

    def create_budget(self, request_dto):
        budget = request_dto.model_dump()
        result = self.budget_collection.insert_one(budget)
        return str(result.inserted_id)

    def get_budget_by_user_id(self, user_id: str):
        doc = self.repo.get_budget_by_user_id(user_id)
        if not doc:
            raise NotFoundException("No budget found for this user.")
        model = document_to_budget_model(doc)
        return budget_model_to_response_dto(model)
