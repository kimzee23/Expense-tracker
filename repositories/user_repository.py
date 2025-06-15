class userRepository:
    def __init__(self, db):
        self.collection = db["users"]  # assumes the collection name is 'users'

    def find_by_email(self, email):
        return self.collection.find_one({"email": email})

    def save(self, user_document):
        result = self.collection.insert_one(user_document)
        return str(result.inserted_id)
