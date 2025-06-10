class userRepository:
    def __init__(self, collecton ):
        self.collecton = collecton
    def find_by_email(self, email):
        return self.collecton.find_one({"email": email})