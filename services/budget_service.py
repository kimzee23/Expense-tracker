class BudgetService:
    def __init__(self, db):
        self.db = db
        self.collection = db["budgets"]

    def create_budget(self, dto):
        data = dto.model_dump()

        user_id = data.get("user_id")
        if not user_id:
            raise ValueError("Missing user_id in budget creation")

        print(f"Saving budget for user: {user_id}")

        result = self.collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "user_id": user_id,
                    "amount": data["amount"],
                    "start_date": data["start_date"],
                    "end_date": data["end_date"]
                }
            },
            upsert=True
        )

        if result.upserted_id:
            return {"status": "created", "id": str(result.upserted_id)}
        else:
            existing = self.collection.find_one({"user_id": user_id})
            return {"status": "updated", "id": str(existing["_id"]) if existing else None}

    def get_budget_by_user_id(self, user_id: str):
        budget = self.collection.find_one({"user_id": user_id})

        if not budget:
            print(f"No budget found for user: {user_id}")
            return {
                "user_id": user_id,
                "amount": 0,
                "start_date": None,
                "end_date": None,
                "id": None
            }

        return {
            "user_id": budget.get("user_id"),
            "amount": budget.get("amount", 0),
            "start_date": budget.get("start_date"),
            "end_date": budget.get("end_date"),
            "id": str(budget.get("_id"))
        }

    def delete_budget_by_user_id(self, user_id):
        result = self.collection.delete_one({"user_id": user_id})
        return result.deleted_count > 0
