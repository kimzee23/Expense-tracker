class BudgetRepository:
    def __init__(self, db):
        self.collection = db.budgets

    def upsert_budget(self, budget_dict):
        user_id = budget_dict["user_id"]

        result = self.collection.update_one(
            {"user_id": user_id},
            {"$set": {
                "amount": budget_dict["amount"],
                "start_date": budget_dict["start_date"],
                "end_date": budget_dict["end_date"],
                "user_id": user_id
            }},
            upsert=True
        )

        if result.upserted_id:
            return {"status": "created", "id": str(result.upserted_id)}
        else:
            existing = self.collection.find_one({"user_id": user_id})
            return {
                "status": "updated",
                "id": str(existing["_id"]) if existing else None
            }

    def get_budget_by_user_id(self, user_id):
        budget = self.collection.find_one({"user_id": user_id})
        if not budget:
            return {
                "user_id": user_id,
                "amount": 0,
                "start_date": None,
                "end_date": None,
                "id": None
            }

        return {
            "id": str(budget["_id"]),
            "user_id": budget["user_id"],
            "amount": budget["amount"],
            "start_date": budget.get("start_date"),
            "end_date": budget.get("end_date")
        }
