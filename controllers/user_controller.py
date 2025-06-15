from flask import Blueprint, request, jsonify, session
from dtos.request.user_Login_Request import UserLoginRequest
from dtos.request.user_register_request import UserRegisterRequest
from services import user_service
from utils.mapper.user_mapper import (
    document_to_user_model_dto,
    user_model_to_response_dto,
)
from services.user_service import UserService
from repositories.user_repository import userRepository
from exceptions.invaild_input_exception import InvalidInputException
from exceptions.user_not_found_exception import UserNotFoundException
from exceptions.incorrect_password_exception import IncorrectPasswordException
from exceptions.user_already_exits_exception import UserAlreadyExistsException
from pydantic import ValidationError

user_bp = Blueprint("user", __name__)


def create_user_controller(db):
    user_controller = Blueprint("user_controller", __name__)
    repo = userRepository(db.users)
    service = UserService(repo)

    @user_bp.route("/login", methods=["POST"])
    def login_user():
        if not request.is_json:
            return jsonify({"error": "Expected application/json"}), 415

        try:
            data = request.get_json()
            login_request = UserLoginRequest(**data)
            user = user_service.login(login_request)

            session["user_id"] = str(user.id)  # ✅ This sets the session
            return jsonify({"message": "Login successful", "redirect": "/dashboard"}), 200  #

        except (ValidationError, UserNotFoundException, IncorrectPasswordException) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal server error"}), 500
    @user_controller.route("/register", methods=["POST"])
    def register_user():
        if not request.is_json:
            return jsonify({'error': 'Unsupported Media Type. Expected application/json.'}), 415

        try:
            payload = request.get_json(force=True)
            print("payload",payload)
            reg_req = UserRegisterRequest(**payload)
            _ = service.register(reg_req)

            user_doc = repo.find_by_email(reg_req.email.strip())
            user_model = document_to_user_model_dto(user_doc)
            session["user_id"]= str(user_model.id)
            return jsonify({
                "message": "User registered successfully",
                "id": str(user_model.id),
                "name": user_model.name,
                "email": user_model.email
            }), 201

        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except InvalidInputException as e:
            return jsonify({"error": e.message}), 400
        except UserAlreadyExistsException as e:
            return jsonify({"error": e.message}), 409
        except Exception as e:
            print("Unexpected register error:", str(e))
            return jsonify({"error": str(e)}), 500

    return user_controller
