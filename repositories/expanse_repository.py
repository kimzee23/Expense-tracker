from config.database import db


from pymongo.collection import Collection
from bson.objectid import ObjectId

class ExpenseRepository:
    def __init__(self, db):
        self.collection: Collection = db["expenses"]

    def create_expense(self, expense_data: dict) -> str:
        result = self.collection.insert_one(expense_data)
        return str(result.inserted_id)

    def get_expense_by_user_id(self, user_id: str):
        return list(self.collection.find({"user_id": user_id}))

    def get_expense_by_id(self, expense_id: str):
        return self.collection.find_one({"_id": ObjectId(expense_id)})

    def update_expense(self, expense_id: str, update_data: dict) -> bool:
        result = self.collection.update_one({"_id": ObjectId(expense_id)}, {"$set": update_data})
        return result.modified_count > 0

    def delete_expense(self, expense_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(expense_id)})
        return result.deleted_count > 0
