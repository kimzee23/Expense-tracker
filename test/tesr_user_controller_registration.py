import unittest
from flask import Flask
from pymongo import MongoClient

from controllers.user_controller import create_user_controller
from werkzeug.security import generate_password_hash


class TestUserControllerRegister(unittest.TestCase):

    def setUp(self):
        self.mongo_client = MongoClient("mongodb://localhost:27017/")
        self.db = self.mongo_client.test_expense_tracker_py
        self.collection = self.db.users
        self.collection.delete_many({})

        self.app = Flask(__name__)
        user_controller = create_user_controller(self.db)
        self.app.register_blueprint(user_controller, url_prefix="/api/v1/users")
        self.client = self.app.test_client()
        self.app.testing = True

    def tearDown(self):
        self.collection.delete_many({})
        self.mongo_client.close()

    def test_register_success(self):
        payload = {
            "name": "Olabisi",
            "email": "Olabisi@gmail.com",
            "password": "ola12345",
            "phone": "08012345678",
            "age": 22
        }
        resp = self.client.post("/api/v1/users/register", json=payload)
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data["email"], "Olabisi@gmail.com")

        doc = self.collection.find_one({"email": "Olabisi@gmail.com"})
        self.assertIsNotNone(doc)

    def test_register_duplicate(self):
        self.collection.insert_one({
            "name": "Ada",
            "email": "ada@gmail.com",
            "phone": "08012345678",
            "age": 22,
            "password": generate_password_hash("secret123")
        })
        payload = {
            "name": "Ada",
            "email": "ada@gmail.com",
            "password": "secret123",
            "phone": "08012345678",
            "age": 22
        }
        resp = self.client.post("/api/v1/users/register", json=payload)
        self.assertEqual(resp.status_code, 409)  #
        self.assertIn("error", resp.get_json())

    def test_register_invalid_input(self):
        payload = {"email": "opeboy@gmail.com"}  # missing name, password, etc.
        resp = self.client.post("/api/v1/users/register", json=payload)
        self.assertEqual(resp.status_code, 400)
