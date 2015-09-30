from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return "Path: %s" % path


print("I'm a server!")
