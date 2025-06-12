from flask import Blueprint, request, jsonify
from pymongo import MongoClient

from dtos.request.user_Login_Request import UserLoginRequest
from dtos.request.user_register_request import UserRegisterRequest
from dtos.response.user_login_response import userLoginResponse
from utils.mapper.user_mapper import (
    document_to_user_model_dto,
    user_model_to_response_dto,
    user_register_request_to_document
)
from services.user_service import UserService
from repositories.user_repository import userRepository
from exceptions.invaild_input_exception import InvaidInputException
from exceptions.user_not_found_exception import UserNotFoundException
from exceptions.incorrect_password_exception import IncorrectPasswordException
from exceptions.user_already_exits_exception import user_already_exits_exception
from pydantic import ValidationError

# user_controller = Blueprint("user_controller", __name__)
def create_user_controller(db):
    user_controller = Blueprint("user_controller", __name__)
    repo = userRepository(db.users)
    service = UserService(repo)

    @user_controller.route("/login", methods=["POST"])
    def login():
        try:
            payload = request.get_json()
            login_req = UserLoginRequest(**payload)
            user_model = service.login(login_req)
            resp_dto = user_model_to_response_dto(user_model)
            return jsonify(resp_dto.dict()), 200
        except InvaidInputException as e:
            return jsonify({"error": e.message}), 400
        except UserNotFoundException as e:
            return jsonify({"error": e.message}), 404
        except IncorrectPasswordException as e:
            return jsonify({"error": e.message}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @user_controller.route("/register", methods=["POST"])
    def register_user():
        try:
            payload = request.get_json()
            reg_req = UserRegisterRequest(**payload)
            new_user_id = service.register(reg_req)

            # fetch the freshly created user
            user_doc = repo.find_by_email(reg_req.email.strip())
            user_model = document_to_user_model_dto(user_doc)
            resp_dto = user_model_to_response_dto(user_model)
            return jsonify(resp_dto.model_dump()), 201
            print(repo_dto.dict)
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except InvaidInputException as e:
            return jsonify({"error": e.message}), 400
        except user_already_exits_exception as e:
            return jsonify({"error": e.message}), 409
        except Exception as e:
            print("Unexpected register error:", str(e))
            return jsonify({"error": str(e)}), 500

    return user_controller

