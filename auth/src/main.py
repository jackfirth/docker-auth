from flask import Flask
from flask import request
from requests import get, put, post, delete, patch
from config import TARGET_SERVICE_HOST, DEBUG_MODE
from proxy import \
    proxy_route, \
    proxy_request, \
    proxy_request_with_body
from authenticate import with_authenticated_identity
from model import initialize_database

app = Flask(__name__)


def target_service_url(path):
    return "http://" + TARGET_SERVICE_HOST + "/" + path


@proxy_route(app)
def catch_all(path):
    def forward_request_as_identity(identity):
        target_url = target_service_url(path)
        new_headers = {"Identity": identity}
        auth_request = proxy_request(target_url, new_headers)
        auth_request_with_body = proxy_request_with_body(
            target_url,
            new_headers
        )
        if request.method == "GET":
            return auth_request(get)
        if request.method == "PUT":
            return auth_request_with_body(put)
        if request.method == "POST":
            return auth_request_with_body(post)
        if request.method == "DELETE":
            return auth_request(delete)
        if request.method == "PATCH":
            return auth_request_with_body(patch)

    return with_authenticated_identity(forward_request_as_identity)

if __name__ == "__main__":
    initialize_database()
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)
