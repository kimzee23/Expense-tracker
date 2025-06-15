from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from dtos.request.user_register_request import UserRegisterRequest
from dtos.request.user_Login_Request import UserLoginRequest
from services.user_service import UserService
from repositories.user_repository import userRepository
from exceptions import (
    invaild_input_exception,
    user_not_found_exception,
    incorrect_password_exception,
    user_already_exits_exception
)
from pydantic import ValidationError


def create_auth_controller(db):
    auth_bp = Blueprint('auth', __name__)
    repo = userRepository(db)
    service = UserService(repo)

    # LANDING PAGE

    @auth_bp.route('/', methods=['GET'])
    def landing():

        return render_template('landing.html')

    @auth_bp.route('/dashboard', methods=['GET'])
    def dashboard():
        return render_template('dashboard.html')

    # AUTHENTICATION

    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():
        """Handle registration"""
        if request.method == 'GET':
            return render_template('register.html')

        try:
            data = request.get_json(force=True)
            register_req = UserRegisterRequest(**data)
            user = service.register(register_req)
            return jsonify({
                'id': str(user.id),
                'email': user.email,
                'username': user.username
            }), 201
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except user_already_exits_exception as e:
            return jsonify({'error': str(e)}), 409
        except Exception as e:
            return jsonify({'error': 'Registration failed'}), 500

    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        """Handling login"""
        if request.method == 'GET':
            return render_template('login.html')

        try:
            data = request.get_json()
            login_req = UserLoginRequest(**data)
            user = service.login(login_req)
            return jsonify({
                'id': str(user.id),
                'email': user.email,
                'token': user.token
            }), 200
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except (user_not_found_exception, incorrect_password_exception) as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': 'Login failed'}), 500

    return auth_bp