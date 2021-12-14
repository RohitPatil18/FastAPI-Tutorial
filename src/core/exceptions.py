class AuthenticationFailed(Exception):
    def __init__(self, code: int = 401, message: str = None):
        self.code = code
        if not message:
            self.message = "Authentication Failed."
        else:
            self.message = message