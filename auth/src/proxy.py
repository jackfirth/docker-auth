from pyramda import compose
from flask import request


allowed_methods = [
    "GET",
    "PUT",
    "POST",
    "DELETE"
]


def proxy_route(app):
    return compose(
        app.route('/', defaults={'path': ''}, methods=allowed_methods),
        app.route('/<path:path>', methods=allowed_methods)
    )


def proxy_request(location, request_func):
    return request_func(
        location,
        params=request.args
    ).content


def proxy_request_with_body(location, request_func):
    return request_func(
        location,
        data=request.get_data(),
        params=request.args
    ).content
