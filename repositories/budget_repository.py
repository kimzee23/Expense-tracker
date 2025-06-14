class BudgetRepository:
    def __init__(self, db):
        self.collection = db.budgets

    def create_budget(self, budget_dict):
        return self.collection.insert_one(budget_dict)

    def get_budget_by_user_id(self, user_id):
        return self.collection.find_one({"user_id": user_id})
