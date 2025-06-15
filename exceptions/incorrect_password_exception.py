class IncorrectPasswordException(Exception):
    def __init__(self, message="Incorrect password"):
        self.message = message
        super().__init__(self.message)
