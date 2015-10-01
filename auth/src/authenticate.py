from flask import request
from db import is_valid_user_email_and_password
from jwt import decode, InvalidTokenError
from config import JWT_SECRET


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


def has_prefix(prefix, string):
    return len(string) >= len(prefix) and string[:len(prefix)] == prefix


def request_auth_type(auth_header):
    if has_prefix("Basic ", auth_header):
        return "Basic"
    if has_prefix("Bearer ", auth_header):
        return "Bearer"
    raise ValueError("Unknown auth header type %s" % auth_header)


def request_auth_data(auth_type, auth_header):
    if auth_type == "Basic":
        return request_basic_auth_data(auth_header)
    if auth_type == "Bearer":
        return request_auth_jwt(auth_header)


def request_basic_auth_data(auth_header):
    auth_parts = auth_header[len("Basic "):].split(":")
    user_email = auth_parts[0]
    password = ":".join(auth_parts[1:])
    return user_email, password


def request_auth_jwt(auth_header):
    return auth_header[len("Bearer "):]


def is_valid_jwt(jwt):
    try:
        decode(jwt, JWT_SECRET, options={"require_email": True})
        return True
    except InvalidTokenError:
        return False


def jwt_email(jwt):
    payload = decode(jwt, JWT_SECRET, options={"require_email": True})
    return payload["email"]


class AuthData:
    def __init__(self, request):
        auth_header = request.headers["Authorization"]
        self.type = request_auth_type(auth_header)
        self.data = request_auth_data(self.type, auth_header)

    def is_valid(self):
        if self.type == "Basic":
            user_email, password = self.data
            return is_valid_user_email_and_password(user_email, password)
        if self.type == "Bearer":
            jwt = self.data
            return is_valid_jwt(jwt)

    def identity(self):
        if self.type == "Basic":
            user_email, password = self.data
            return "Email " + user_email
        if self.type == "Bearer":
            jwt = self.data
            return "Email " + jwt_email(jwt)

    def failure_response(self):
        if self.type == "Basic":
            return "Invalid username and/or password"
        if self.type == "Bearer":
            return "Invalid token"


def authenticate():
    auth_data = AuthData(request)
    if auth_data.is_valid():
        identity = auth_data.identity()
        return Authentication(True, identity=identity)
    else:
        failure_response = auth_data.failure_response()
        return Authentication(False, failure_response=failure_response)
