from werkzeug.security import generate_password_hash

from dtos.request.user_register_request import UserRegisterRequest
from dtos.response.user_RegisterResponse import UserRegisterResponse
from dtos.response.user_login_response import userLoginResponse
from  models.user_model import UserModel

def  document_to_user_model_dto(doc):
    return UserModel(
        id=str(doc["_id"]),
        name=doc["name"],
        email=doc["email"],
        phone=doc["phone"],
        age=doc["age"],
        password=doc["password"]
    )

def user_model_to_response_dto(user: UserModel) -> UserRegisterResponse:
    return UserRegisterResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        phone=user.phone,
        age=user.age
    )
def user_register_request_to_document(req: UserRegisterRequest) -> dict:
    hashed = generate_password_hash(req.password.strip())
    return {
        "name": req.name.strip(),
        "email": req.email.strip(),
        "password": hashed,
        "phone": req.phone.strip(),
        "age": req.age
    }