from os import environ


required_var_msg_format = "No value for required environment variable {0}"
optional_var_msg_format = \
    "No value for optional environment variable {0}, default to {1}"


def checked_environ(var_name):
    if var_name not in environ:
        raise EnvironmentError(required_var_message_format % var_name)
    return environ[var_name]


def default_environ(default_value, var_name):
    if var_name not in environ:
        print(optional_var_msg_format.format(var_name, default_value))
        return default_value
    return environ[var_name]

TARGET_SERVICE_HOST = checked_environ("TARGET_SERVICE_HOST")
DEBUG_MODE = checked_environ("DEBUG_MODE") == "true"
DB_USER = checked_environ("DB_USER")
DB_PASSWORD = checked_environ("DB_PASSWORD")
DB_HOST = checked_environ("DB_HOST")
DB_SCHEMA = checked_environ("DB_SCHEMA")
JWT_SECRET = checked_environ("JWT_SECRET")
HASH_ROUNDS = default_environ(40000, "HASH_ROUNDS")
