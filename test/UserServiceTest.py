import unittest
from pymongo import MongoClient
from services.user_service import UserService
from dtos.request.user_Login_Request import UserLoginRequest
from werkzeug.security import generate_password_hash
from pydantic import ValidationError
from repositories.user_repository import userRepository
from exceptions.incorrect_password_exception import IncorrectPasswordException


class TestUserServiceMongo(unittest.TestCase):
    def setUp(self):

        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client.test_expense_tracker_py
        self.collection = self.db.users
        self.collection.delete_many({})

        self.repo = userRepository(self.collection)
        self.service = UserService(self.repo)

        self.collection.insert_one({
            "name": "Ade",
            "email": "ade@gmail.com",
            "phone": "+2348115016091",
            "age": 28,
            "password": generate_password_hash("pass123")
        })

    def tearDown(self):
        self.collection.delete_many({})
        self.client.close()

    def test_login_success(self):
        login_request = UserLoginRequest(email="ade@gmail.com", password="pass123")
        user = self.service.login(login_request)
        self.assertEqual(user.name, "Ade")
        self.assertEqual(user.email, "ade@gmail.com")

    def test_login_invalid_email_format(self):
        with self.assertRaises(ValidationError):
            # 👇 This will fail validation before hitting service
            UserLoginRequest(email="", password="")

    def test_login_incorrect_password(self):
        login_request = UserLoginRequest(email="ade@gmail.com", password="wrongpass")
        with self.assertRaises(IncorrectPasswordException):
            self.service.login(login_request)


if __name__ == '__main__':
    unittest.main()
