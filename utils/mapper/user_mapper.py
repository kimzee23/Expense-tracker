from  models.user_model import UserModel

def document_to_user_model(doc):
    return UserModel(
        id=str(doc["_id"]),
        name=doc["name"],
        email=doc["email"],
        phone=doc["phone"],
        age=doc["age"],
        password=doc["password"],

    )