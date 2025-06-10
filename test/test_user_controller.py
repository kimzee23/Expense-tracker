from unittest import TestCase
from pymongo import MongoClient

from dtos.request.userLoginRequest import UserLoginRequest
from repositories.user_repository import userRepository
from services.user_service import UserService


class testserviceIntegrationTest(TestCase):
    def setUp(self):
        client = MongoClient("mongodb://localhost:27017/")
        self.db = client.expense_tracker_test
        self.db.users.drop()

        self.db.users.insert_one({
            "name": "Ade",
            "email": "ade@gmail.com",
            "phone": "+23408115016091",
            "age": 24,
            "password": "pass432"
        })
        self.service = UserService(userRepository(self.db.users))
    def tearDown(self):
        self.db.users.drop()

    def test_login_end_to_end(self):
        request = UserLoginRequest(email="ade@gmail.com", password="pass432")
        user = self.service.login(request)
        self.assertEqual(user.email, "ade@gmail.com")
