from flask import Blueprint, request, render_template, redirect, session, jsonify
from dtos.request.user_register_request import UserRegisterRequest
from dtos.request.user_Login_Request import UserLoginRequest
from exceptions.UserAlreadyExitsException import UserAlreadyExistsException
from exceptions.incorrect_password_exception import IncorrectPasswordException
from exceptions.user_not_found_exception import UserNotFoundException
from exceptions.invaild_input_exception import InvalidInputException
from services.user_service import UserService
from repositories.user_repository import userRepository
from pydantic import ValidationError
import traceback

def create_auth_controller(db):
    auth_bp = Blueprint('auth', __name__)
    repo = userRepository(db)
    service = UserService(repo)

    @auth_bp.route('/', methods=['GET'])
    def landing():
        return render_template('landing.html')

    @auth_bp.route('/dashboard', methods=['GET'])
    def dashboard():
        if 'user_id' not in session:
            return redirect('/login')
        return render_template('dashboard.html')

    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():  # ✅ Matches url_for('auth.register')
        if request.method == 'GET':
            return render_template('register.html')
        try:
            data = request.form
            age_value = data.get('age')
            if not age_value:
                raise InvalidInputException("Age is required")

            register_req = UserRegisterRequest(
                name=data.get('name'),
                email=data.get('email'),
                password=data.get('password'),
                phone=data.get('phone'),
                age=int(age_value)
            )
            user_id = service.register(register_req)
            session['user_id'] = str(user_id)
            return redirect('/dashboard')
        except (ValidationError, UserAlreadyExistsException, InvalidInputException) as e:
            return render_template('register.html', error=str(e))
        except Exception:
            traceback.print_exc()
            return render_template('register.html', error="Something went wrong")

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
                age=int(data.get('age'))
            )
            user_id = service.register(register_req)
            session['user_id'] = str(user_id)
            return jsonify({
                "message": "Registration successful",
                "user_id": str(user_id)
            }), 201
        except (ValidationError, UserAlreadyExistsException) as e:
            return jsonify({"error": str(e)}), 400
        except Exception:
            traceback.print_exc()
            return jsonify({"error": "Something went wrong"}), 500

    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():  # ✅ Matches url_for('auth.login')
        if request.method == 'GET':
            return render_template('login.html')
        try:
            data = request.form
            login_req = UserLoginRequest(
                email=data.get('email'),
                password=data.get('password')
            )
            user_id = service.login(login_req)
            session['user_id'] = str(user_id)
            return redirect('/dashboard')
        except (ValidationError, UserNotFoundException, IncorrectPasswordException) as e:
            return render_template('login.html', error=str(e))
        except Exception:
            traceback.print_exc()
            return render_template('login.html', error="Something went wrong")

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
            user_id = service.login(login_req)
            session['user_id'] = str(user_id)
            return jsonify({
                "message": "Login successful",
                "user_id": str(user_id)
            }), 200
        except UserNotFoundException:
            return jsonify({"error": "User not found"}), 404
        except IncorrectPasswordException:
            return jsonify({"error": "Incorrect password"}), 401
        except ValidationError:
            return jsonify({"error": "Invalid input"}), 400
        except Exception as e:
            print("Unexpected error:", e)
            return jsonify({"error": "Something went wrong"}), 500

    return auth_bp
