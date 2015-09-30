from flask import Flask
from flask import request
from config import TARGET_SERVICE_HOST, DEBUG_MODE
from requests import get, put, post, delete

app = Flask(__name__)

allowed_methods = [
    "GET",
    "PUT",
    "POST",
    "DELETE"
]


def target_service_url(path):
    return "http://" + TARGET_SERVICE_HOST + "/" + path


def proxy_pass_method(location, method_func):
    return method_func(
        location,
        params=request.args
    ).content


def proxy_pass_method_with_body(location, method_func):
    return method_func(
        location,
        data=request.get_data(),
        params=request.args
    ).content


@app.route('/', defaults={'path': ''}, methods=allowed_methods)
@app.route('/<path:path>', methods=allowed_methods)
def catch_all(path):
    target_url = target_service_url(path)
    if request.method == "GET":
        return proxy_pass_method(target_url, get)
    if request.method == "PUT":
        return proxy_pass_method_with_body(target_url, put)
    if request.method == "POST":
        return proxy_pass_method_with_body(target_url, post)
    if request.method == "DELETE":
        return proxy_pass_method(target_url, delete)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
