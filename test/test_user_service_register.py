import unittest
from unittest.mock import MagicMock

from flask import request
from bson import  ObjectId
from pydantic_core import ValidationError

from dtos.request.user_register_request import UserRegisterRequest
from exceptions.user_already_exits_exception import user_already_exits_exception
from services.user_service import UserService


class TestUserServiceRegister(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = UserService(self.mock_repo)

    def test_that_registration_is_successful(self):
        self.mock_repo.find_by_email.return_value = None
        register = UserRegisterRequest(
            name="Olabisi",
            email="Olabisi@gmail.com",
            age=22,
            phone= "08115016091",
            password="Ola12345",
        )
        fake_object_id = ObjectId()
        self.mock_repo.save.return_value = fake_object_id

        new_id = self.service.register(register)

        self.assertEqual(new_id, str(fake_object_id))
        print(fake_object_id)
        print(new_id)
        # self.mock_repo.save.assert_called_once()
    def test_if_user_enter_invaild_input(self):
        with self.assertRaises(ValidationError):
            UserRegisterRequest(
                name="O",
                email= "mail",
                phone="",
                age=-1,
                password="1234",
            )
    def test_if_registration_is_dulicated(self):
        self.mock_repo.find_by_email.return_value = {"-id":"68495519909fe3f420c064f5","email":"Olabisi@gmail.com"}
        register = UserRegisterRequest(
            name="Olabisi",
            email="Olabisi@gmail.com",
            phone="+2348115016091",
            password="Ola12345",
            age=22,
        )
        with self.assertRaises( user_already_exits_exception):
            print(user_already_exits_exception(register))
            self.service.register(register)
if __name__ == '__main__':
    unittest.main()

