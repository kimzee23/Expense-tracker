from pymongo import MongoClient

class ReportRepository:
    def __init__(self, db):
        self.reports = db["reports"]
        self.expenses = db["expenses"]

    def save(self, report_dict):
        result = self.reports.insert_one(report_dict)
        return str(result.inserted_id)

    def find_by_user_id(self, user_id: str):
        return self.reports.find_one({"user_id": user_id})

    def get_expenses_by_user_id(self, user_id: str):
        return list(self.expenses.find({"user_id": user_id}))
