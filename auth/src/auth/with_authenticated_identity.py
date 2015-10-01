from .authenticate import authenticate


def with_authenticated_identity(handler):
    auth = authenticate()
    if auth.successful:
        return handler(auth.identity)
    else:
        return auth.failure_response
