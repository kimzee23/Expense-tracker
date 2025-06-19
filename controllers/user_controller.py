from flask import Blueprint, request, jsonify, session
from dtos.request.user_Login_Request import UserLoginRequest
from dtos.request.user_register_request import UserRegisterRequest
from exceptions.not_found_exception import NotFoundException
from exceptions.invaild_input_exception import InvalidInputException
from exceptions.user_not_found_exception import UserNotFoundException
from exceptions.incorrect_password_exception import IncorrectPasswordException
from exceptions.UserAlreadyExitsException import UserAlreadyExistsException
from pydantic import ValidationError

from services.user_service import UserService
from repositories.user_repository import userRepository

def create_user_controller(db):
    user_controller = Blueprint("user_controller", __name__)
    repo = userRepository(db.users)
    service = UserService(repo)

    @user_controller.route("/login", methods=["POST"])
    def login_user():
        try:
            data = request.get_json()
            user_dto = UserLoginRequest(**data)
            user = service.login_user(user_dto)

            # Set user_id in session so frontend can redirect
            session['user_id'] = str(user.id)

            return jsonify({
                "message": "Login successful",
                "user_id": str(user.id),
                "user": {
                    "name": user.name,
                    "email": user.email,
                    "id": str(user.id)
                }
            }), 200
        except (UserNotFoundException, NotFoundException) as e:
            return jsonify({"error": str(e)}), 404
        except IncorrectPasswordException as e:
            return jsonify({"error": str(e)}), 401
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500


    @user_controller.route("/register", methods=["POST"])
    def register_user():
        try:
            data = request.get_json()
            user_dto = UserRegisterRequest(**data)
            user = service.register_user(user_dto)

            # Set session immediately after registration
            session['user_id'] = str(user.id)

            return jsonify({
                "message": "User registered successfully",
                "user_id": str(user.id),
                "use ;zcsdljvr": {
                    "name": user.name,
                    "email": user.email,
                    "id": str(user.id)
                }
            }), 201
        except UserAlreadyExistsException as e:
            return jsonify({"error": str(e)}), 409
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    return user_controller
