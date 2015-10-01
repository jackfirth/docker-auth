from os import environ


def checked_environ(var_name):
    if var_name not in environ:
        raise EnvironmentError(
            "No value for required environment variable {0}" % var_name
        )
    return environ[var_name]

TARGET_SERVICE_HOST = checked_environ("TARGET_SERVICE_HOST")
DEBUG_MODE = checked_environ("DEBUG_MODE") == "true"
DB_USER = checked_environ("DB_USER")
DB_PASSWORD = checked_environ("DB_PASSWORD")
DB_HOST = checked_environ("DB_HOST")
DB_SCHEMA = checked_environ("DB_SCHEMA")
