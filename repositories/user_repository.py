class userRepository:
    def __init__(self, collecton ):
        self.collecton = collecton

    def find_by_email(self, email):
        return self.collecton.find_one({"email": email})

    def save(self, user_document):
        result = self.collecton.insert_one(user_document)
        return str(result.inserted_id)