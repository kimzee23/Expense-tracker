import unittest
from app import create_app
from pymongo import MongoClient

class TestReportController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = MongoClient("mongodb://localhost:27017/")
        cls.test_db = cls.client["test_expense_tracker"]
        cls.app = create_app(cls.test_db).test_client()

    def setUp(self):
        self.test_db = self.client["test_expense_tracker"]
        self.test_db["reports"].delete_many({})

    def test_create_report_success(self):
        data = {
            "user_id": "1234yx",
            "title": "Weekly Summary",
            "description": "Spent a lot this week",
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "total_budget": 500.0,
            "total_expense": 450.0,
            "total_income": 700.0
        }

        response = self.app.post("/api/v1/reports/", json=data)
        print("Response JSON:", response.get_json())
        self.assertEqual(response.status_code, 201)
        self.assertIn("title", response.get_json())
        self.assertIn("generated_at", response.get_json())

    def test_generate_at(self):
        dataTwo = {
            "user_id": "123ux",
            "title": "Weekly Summary",
            "description": "Spent a lot this week",
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "total_budget": 500.0,
            "total_expense": 450.0,
            "total_income": 700.0
        }

        response = self.app.post("/api/v1/reports/", json=dataTwo)
        print("Response JSON:", response.get_json())
        self.assertEqual(response.status_code, 201)
        self.assertIn("generated_at", response.get_json())
        print(response.get_json())



    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database("test_expense_tracker")
        cls.client.close()
