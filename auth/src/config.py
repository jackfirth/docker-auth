from pyramda import identity, compose
from env import default_environ, required_environ, pred_environ


default_hash_algoirthm = "pbkdf2_sha512"
allowed_hash_algorithms = [
    default_hash_algoirthm
]


def is_hash_alg(v):
    return v in allowed_hash_algorithms


def is_int_string(v):
    if not isinstance(v, str):
        return False
    try:
        int(v)
        return True
    except ValueError:
        return False


def is_bool_string(v):
    return v == "true" or v == "false"


def bool_string_to_bool(bool_string):
    return bool_string == "true"


int_string_environ = pred_environ(
    is_int_string,
    int,
    "an integer"
)

bool_string_environ = pred_environ(
    is_bool_string,
    bool_string_to_bool,
    "either 'true' or 'false'"
)

hash_alg_environ = pred_environ(
    is_hash_alg,
    identity,
    "one of {0}" % allowed_hash_algorithms
)

default_hash_alg_environ = compose(
    hash_alg_environ,
    default_environ(default_hash_algoirthm)
)

default_hash_rounds_environ = compose(
    int_string_environ,
    default_environ("40000")
)

min_password_length_environ = compose(
    int_string_environ,
    default_environ("12")
)

TARGET_SERVICE_HOST = required_environ("TARGET_SERVICE_HOST").value
DB_USER = required_environ("DB_USER").value
DB_PASSWORD = required_environ("DB_PASSWORD").value
DB_HOST = required_environ("DB_HOST").value
DB_SCHEMA = required_environ("DB_SCHEMA").value
JWT_SECRET = required_environ("JWT_SECRET").value
HASH_ROUNDS = default_hash_rounds_environ("HASH_ROUNDS").value
HASH_ALGORITHM = default_hash_alg_environ("HASH_ALGORITHM").value
DEBUG_MODE = bool_string_environ(required_environ("DEBUG_MODE")).value
MIN_PASSWORD_LENGTH = min_password_length_environ("MIN_PASSWORD_LENGTH").value
