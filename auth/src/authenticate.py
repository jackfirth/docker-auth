from flask import request
from auth_db import is_valid_user_email_and_password


def with_authenticated_identity(handler):
    auth = authenticate()
    if auth.successful:
        return handler(auth.identity)
    else:
        return auth.failure_response


class Authentication:
    def __init__(self, successful, failure_response=None, identity=None):
        self.successful = successful
        self.failure_response = failure_response
        self.identity = identity
        if successful and failure_response:
            raise ValueError("Can't provide failure response if successful")
        if not successful and identity:
            raise ValueError("Can't provide identity if not successful")


def authenticate():
    auth_data = request_auth_data(request)
    if is_valid_auth_data(auth_data):
        identity = auth_identity(auth_data)
        return Authentication(True, identity=identity)
    else:
        failure_response = auth_failure_response(auth_data)
        return Authentication(False, failure_response=failure_response)


def request_auth_data(request):
    auth_header = request.headers["Authorization"]
    auth_parts = auth_header[len("Basic "):].split(":")
    user_email = auth_parts[0]
    password = ":".join(auth_parts[1:])
    return user_email, password


def is_valid_auth_data(auth_data):
    user_email, password = auth_data
    return is_valid_user_email_and_password(user_email, password)


def auth_identity(auth_data):
    user_email, password = auth_data
    return "Email " + user_email


def auth_failure_response(auth_data):
    user_email, password = auth_data
    return "Invalid username and/or password"
