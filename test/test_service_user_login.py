from unittest import TestCase

import flask
from flask import Flask
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from controllers.user_controller import create_user_controller
from dtos.request.user_Login_Request import UserLoginRequest
from repositories.user_repository import userRepository
from utils.mapper.user_mapper import document_to_user_model_dto
from services.user_service import UserService


class testserviceIntegrationTest(TestCase):
    def setUp(self):
        self.mongo_client = MongoClient("mongodb://localhost:27017/")
        self.db = self.mongo_client.expense_tracker_test
        self.db.users.drop()
        password_hashed = generate_password_hash("pass432")
        self.db.users.insert_one({
            "name": "Ade",
            "email": "ade@gmail.com",
            "phone": "+23408115016091",
            "age": 24,
            "password": password_hashed,
        })
        self.service = UserService(userRepository(self.db.users))
    def tearDown(self):
        self.db.users.drop()
        self.mongo_client.close()

    def test_login_end_to_end(self):
        request = UserLoginRequest(email="ade@gmail.com", password="pass432")
        user = self.service.login(request)
        self.assertEqual(user.email, "ade@gmail.com")
        self.assertEqual(user.name, "Ade")
