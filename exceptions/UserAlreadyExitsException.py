class UserAlreadyExistsException(Exception):
    def __init__(self, message="A user already exists"):
        self.message = message
        super().__init__(self.message)
