from exceptions.not_found_exception import NotFoundException
from repositories.budget_repository import BudgetRepository
from utils.mapper.budget_mapper import document_to_budget_model, budget_model_to_response_dto


from exceptions.not_found_exception import NotFoundException

class BudgetService:
    def __init__(self, db):
        self.db = db
        self.collection = db["budgets"]

    def create_budget(self, dto):
        data = dto.model_dump()

        # Upsert: if budget already exists, update it
        result = self.collection.update_one(
            {"user_id": data["user_id"]},
            {"$set": {"amount": data["amount"]}},
            upsert=True
        )
        return str(result.upserted_id or "updated")

    def get_budget_by_user_id(self, user_id: str):
        budget = self.collection.find_one({"user_id": user_id})
        if not budget:
            raise NotFoundException("No budget found for this user")
        return {"user_id": budget["user_id"], "amount": budget["amount"]}

