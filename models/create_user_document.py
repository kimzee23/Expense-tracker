from werkzeug.security import generate_password_hash



def create_user_document(register_request):
    return {
        "name": register_request.name,
        "email": register_request.email,
        "phone": register_request.phone,
        "age": register_request.age,
        "password": generate_password_hash(register_request.password)
    }

