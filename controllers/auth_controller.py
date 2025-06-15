from flask import Blueprint, request, render_template, redirect, session, jsonify
from dtos.request.user_register_request import UserRegisterRequest
from dtos.request.user_Login_Request import UserLoginRequest
from exceptions.user_already_exits_exception import UserAlreadyExistsException
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

    # Landing Page
    @auth_bp.route('/', methods=['GET'])
    def landing():
        return render_template('landing.html')

    # Dashboard (protected)
    @auth_bp.route('/dashboard', methods=['GET'])
    def dashboard():
        if 'user_id' not in session:
            return redirect('/login')
        return render_template('dashboard.html')

    # Form-based Register
    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('register.html')
        try:
            data = request.form
            register_req = UserRegisterRequest(
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password')
            )
            user = service.register(register_req)
            session['user_id'] = str(user.id)
            return redirect('/dashboard')
        except (ValidationError, user_already_exits_exception, Exception):
            return render_template('register.html', error="Registration failed")

    # Form-based Login
    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        try:
            data = request.form
            login_req = UserLoginRequest(
                email=data.get('email'),
                password=data.get('password')
            )
            user = service.login(login_req)
            session['user_id'] = str(user.id)
            return redirect('/dashboard')
        except (ValidationError, user_not_found_exception, incorrect_password_exception, Exception):
            return render_template('login.html', error="Invalid login")

    # JSON API - Register via JS fetch()
    @auth_bp.route('/api/v1/users/register', methods=['POST'])
    def api_register():
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        try:
            data = request.get_json()
            register_req = UserRegisterRequest(
                name=data.get('name'),
                email=data.get('email'),
                password=data.get('password'),
                phone=data.get('phone'),
                age=data.get('age')
            )
            user = service.register(register_req)
            session['user_id'] = str(user.id)
            return jsonify({"message": "Registration successful", "redirect": "/dashboard"}), 201
        except (ValidationError, UserAlreadyExistsException) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Something went wrong"}), 500

    # JSON API - Login via JS fetch()
    @auth_bp.route('/api/v1/users/login', methods=['POST'])
    def api_login():
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        try:
            data = request.get_json()
            login_req = UserLoginRequest(
                email=data.get('email'),
                password=data.get('password')
            )
            user = service.login(login_req)
            session['user_id'] = str(user.id)
            return jsonify({"message": "Login successful", "redirect": "/dashboard"}), 200
        except (ValidationError, user_not_found_exception, incorrect_password_exception) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Something went wrong"}), 500

    return auth_bp
