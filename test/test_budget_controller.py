
import unittest
from pymongo import MongoClient
from app import create_app

class BudgetControllerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        client = MongoClient("mongodb://localhost:27017/")
        cls.test_db = client["expense_tracker_test_py"]  # this is your test DB
        cls.app = create_app(cls.test_db)
        cls.client = cls.app.test_client()

    # def setUp(self):
    #     self.test_db.budgets.delete_many({})

    def test_create_budget(self):
        response = self.client.post("/api/v1/budgets", json={
            "user_id": "user123",
            "amount": 5000,
            "start_date": "2025-06-01",
            "end_date": "2025-06-30"
        })
        print("Status Code:", response.status_code)
        print("Response JSON:", response.get_json())

        self.assertEqual(response.status_code, 201)
        self.assertIn("budget_id", response.get_json())

    def test_get_budget_by_user_id(self):
        self.test_db.budgets.insert_one({
            "user_id": "user123",
            "amount": 5000,
            "start_date": "2025-06-01",
            "end_date": "2025-06-30"
        })
        response = self.client.get("/api/v1/budgets/user123")
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_id", response.get_json())

if __name__ == "__main__":
    unittest.main()
