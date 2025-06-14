from pymongo import MongoClient


class ReportRepository:
    def __init__(self, db):
        self.collection = db["reports"]


    def save(self, report_dict):
        result = self.collection.insert_one(report_dict)
        return str(result.inserted_id)

    def find_by_user_id(self, user_id: str):
        return self.collection.find_one({"user_id": user_id})
