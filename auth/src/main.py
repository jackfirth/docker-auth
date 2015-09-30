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


@app.route('/', defaults={'path': ''}, methods=allowed_methods)
@app.route('/<path:path>', methods=allowed_methods)
def catch_all(path):
    target_url = "http://" + TARGET_SERVICE_HOST + "/" + path
    if request.method == "GET":
        return get(target_url).content
    if request.method == "PUT":
        return put(target_url, data=request.get_data()).content
    if request.method == "POST":
        return post(target_url, data=request.get_data()).content
    if request.method == "DELETE":
        return delete(target_url).content


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
