from flask import Flask
from flask import request
from requests import get, put, post, delete, patch
from config import \
    TARGET_SERVICE_HOST, \
    DEBUG_MODE, \
    MIN_PASSWORD_LENGTH, \
    PASSWORD_CHAR_SET, \
    PASSWORD_CHAR_SET_NAME
from proxy import \
    proxy_route, \
    proxy_request, \
    proxy_request_with_body
from auth import with_authenticated_identity
from db import initialize_database, create_user
from pyramda import getattr, getitem, compose

app = Flask(__name__)


def target_service_url(path):
    return "http://" + TARGET_SERVICE_HOST + "/" + path


def has_disallowed_chars(password):
    if PASSWORD_CHAR_SET is None:
        return False
    for char in password:
        if char not in PASSWORD_CHAR_SET:
            return True
    return False


@app.route("/auth/signup", methods=["POST"])
def signup():
    app.logger.info("Signing up new user")
    user_email = get_request_email(request)
    password = get_request_password(request)
    if len(password) < MIN_PASSWORD_LENGTH:
        app.logger.info(
            "User {0}'s provided password was too short ({1} chars)".format(
                user_email,
                len(password)
            )
        )
        return "Password too short, has length {0} but minimum is {1}".format(
            len(password),
            MIN_PASSWORD_LENGTH
        ), 400
    if has_disallowed_chars(password):
        log_format = "User {0}'s provided password has disallowed characters"
        app.logger.info(log_format.format(user_email))
        msg_format = \
            "Password contains disallowed characters, only {0} supported"
        return msg_format.format(PASSWORD_CHAR_SET_NAME), 400
    create_user(user_email, password)
    return ""


@proxy_route(app)
def catch_all(path):
    def forward_request_as_identity(identity):
        target_url = target_service_url(path)
        new_headers = {
            "Identity": identity
        }
        if "Content-Type" in request.headers:
            new_headers["Content-Type"] = request.headers["Content-Type"]
        if "Accept" in request.headers:
            new_headers["Accept"] = request.headers["Accept"]
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

    app.logger.info("Proxying to route %s" % path)
    return with_authenticated_identity(forward_request_as_identity)


request_json = getattr("json")
get_request_email = compose(getitem("email"), request_json)
get_request_password = compose(getitem("password"), request_json)

if __name__ == "__main__":
    initialize_database()
    app.run(host='0.0.0.0', port=8000, debug=DEBUG_MODE, use_reloader=False)
