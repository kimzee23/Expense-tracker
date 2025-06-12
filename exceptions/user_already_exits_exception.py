class user_already_exits_exception(Exception):
    def __init__(self, message="A user already exists already Exits"):
        self.message = message
        super().__init__(self.message)
