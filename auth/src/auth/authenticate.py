from flask import request
from jwt import decode, InvalidTokenError
from .protocol import first_protocol_matching


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
    protocol = first_protocol_matching(request.headers["Authorization"])
    if protocol.is_valid():
        identity = protocol.identity()
        return Authentication(True, identity=identity)
    else:
        failure_response = protocol.failure_response()
        return Authentication(False, failure_response=failure_response)
