class InvaidInputException(Exception):
    def __init__(self, message="Invalid input "):
        self.message = message
        super().__init__(self.message)