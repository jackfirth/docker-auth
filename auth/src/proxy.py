from pyramda import compose, curry
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


@curry
def proxy_request(location, headers, request_func):
    return request_func(
        location,
        params=request.args,
        headers=headers
    ).content


@curry
def proxy_request_with_body(location, headers, request_func):
    return request_func(
        location,
        data=request.get_data(),
        params=request.args,
        headers=headers
    ).content
