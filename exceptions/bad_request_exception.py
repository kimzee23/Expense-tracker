class BadRequestException(Exception):
    def __init__(self, message="Bad request"):
        self.message = message
        super().__init__(self.message)
