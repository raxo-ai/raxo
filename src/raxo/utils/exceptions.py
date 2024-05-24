class APIError(Exception):
    pass


class PromptError(Exception):
    pass


class InvalidKeysException(Exception):
    def __init__(self, message="Invalid keys provided in the dictionary"):
        self.message = message
        super().__init__(self.message)

class NoTextProvided(Exception):
    def __init__(self, message="Please provide a valid input"):
        self.message = message
        super().__init__(self.message)
