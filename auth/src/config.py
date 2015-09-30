from os import environ
TARGET_SERVICE_HOST = environ["TARGET_SERVICE_HOST"]
DEBUG_MODE = environ["DEBUG_MODE"] == "true"
