from config.database import db
from bson import ObjectId


class ExpenseRepository:
    def __init__(self):
        self.collection =db.expenses
    def save(self,expense_dict:dict) -> str:
        result = self.collection.insert_one(expense_dict)
        return str(result.inserted_id)

    def find_by_id(self,expense_id:str) -> dict:
        try:
            result = self.collection.find_one({"_id": ObjectId(expense_id)})
        except Exception as e:
            return None
    def find_by_user_id(self,user_id:str) -> list[dict]:
        return list(self.collection.find({"_id": ObjectId(user_id)}))

    def update(self, expense_id: str, update_fields: dict) -> bool:
        result =self.collection.update_one(
            {"_id": ObjectId(expense_id)},
            {"$set": update_fields},
        )
        return result.modified_count > 0

    def delete(self, expense_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(expense_id)})
        return result.deleted_count > 0