from .protocol_basic import BasicAuthProtocol
from .protocol_jwt import JWTAuthProtocol


protocols = [
    BasicAuthProtocol,
    JWTAuthProtocol
]


def first_protocol_matching(auth_header):
    for protocol in protocols:
        if protocol.matches_header(auth_header):
            return protocol(auth_header)
    raise ValueError("No matching protocol for header %s" % auth_header)
