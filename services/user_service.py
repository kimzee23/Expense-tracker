from models.user_model import UserModel
from exceptions.UserAlreadyExitsException import UserAlreadyExistsException
from utils.mapper.user_mapper import document_to_user_model_dto, user_register_request_to_document
from werkzeug.security import check_password_hash, generate_password_hash
from exceptions.incorrect_password_exception import IncorrectPasswordException
from exceptions.user_not_found_exception import UserNotFoundException
from exceptions.invaild_input_exception import InvalidInputException

class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def register(self, register_request) -> str:
        if not register_request.name or not register_request.email or not register_request.password:
            raise InvalidInputException("You need to fill in all fields pal")
        existing_user = self.user_repo.find_by_email(register_request.email.strip())
        if existing_user:
            raise UserAlreadyExistsException("User already exists")

        hashed_password = generate_password_hash(register_request.password.strip())
        user_document = user_register_request_to_document(register_request)
        user_document["password"] = hashed_password

        user_id = self.user_repo.save(user_document)
        return str(user_id)

    def login(self, login_request):
        login_request.email = login_request.email.strip()
        if not login_request.email or not login_request.password:
            raise InvalidInputException("Email and password are required")

        user_doc = self.user_repo.find_by_email(login_request.email)
        if not user_doc:
            raise UserNotFoundException("User not found")

        user_model = document_to_user_model_dto(user_doc)
        if not check_password_hash(user_model.password, login_request.password):
            raise IncorrectPasswordException("Incorrect password")

        return str(user_model.id)
