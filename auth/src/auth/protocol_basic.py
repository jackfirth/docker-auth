from db import is_valid_user_email_and_password
from .has_prefix import has_prefix


class BasicAuthProtocol:
    def matches_header(auth_header):
        return has_prefix("Basic ", auth_header)

    def __init__(self, auth_header):
        self.email, self.password = basic_auth_request_data(auth_header)

    def is_valid(self):
        return is_valid_user_email_and_password(self.email, self.password)

    def identity(self):
        return "Email " + self.email

    def failure_response(self):
        return "Invalid username and/or password"


def basic_auth_request_data(auth_header):
    auth_parts = auth_header[len("Basic "):].split(":")
    user_email = auth_parts[0]
    password = ":".join(auth_parts[1:])
    return user_email, password
