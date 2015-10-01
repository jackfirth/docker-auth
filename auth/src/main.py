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
        if request.method == "GET":
            return proxy_request(target_url, get)
        if request.method == "PUT":
            return proxy_request_with_body(target_url, put)
        if request.method == "POST":
            return proxy_request_with_body(target_url, post)
        if request.method == "DELETE":
            return proxy_request(target_url, delete)
        if request.method == "PATCH":
            return proxy_request_with_body(target_url, patch)
    return with_authenticated_identity(forward_request_as_identity)

if __name__ == "__main__":
    initialize_database()
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)
