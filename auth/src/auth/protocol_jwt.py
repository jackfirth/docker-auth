from jwt import decode, InvalidTokenError
from config import JWT_SECRET
from .has_prefix import has_prefix


class JWTAuthProtocol:
    def matches_header(auth_header):
        return has_prefix("Bearer ", auth_header)

    def __init__(self, auth_header):
        self.jwt = jwt_auth_request_data(auth_header)

    def is_valid(self):
        return is_valid_jwt(self.jwt)

    def identity(self):
        return "Email " + jwt_email(self.jwt)

    def failure_response(self):
        return "Invalid token"


def jwt_auth_request_data(auth_header):
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
