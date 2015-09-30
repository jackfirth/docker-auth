from flask import Flask
from flask import request
from config import TARGET_SERVICE_HOST, DEBUG_MODE
from requests import get

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return get("http://" + TARGET_SERVICE_HOST + "/" + path).content


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=DEBUG_MODE)
