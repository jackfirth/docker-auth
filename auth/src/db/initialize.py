from time import sleep
from sys import stdout
from sqlalchemy.exc import OperationalError
from .model import UserAuth, create_tables
from .session import with_session
from .create_model import create_model
from .crypto import encrypt


def with_repeat_on_error(exn_type, num_times, retryable_func):
    for n in range(num_times):
        try:
            return retryable_func(n)
        except exn_type:
            if n == num_times-1:
                raise


create_user_auth = create_model(UserAuth)


def seed_user():
    with_session(create_user_auth({
        "email": "foo@bar.com",
        "password": encrypt("password")
    }))


def initialize_database():
    print("Initializing database")

    def create_tables_with_sleep(num_times_tried):
        print("Attempting database connection...")
        stdout.flush()
        sleep(num_times_tried + 1)
        create_tables()
        print("Succesfully connected, schema initialized")
        stdout.flush()

    with_repeat_on_error(OperationalError, 4, create_tables_with_sleep)
    seed_user()
    print("Successfully seeded, database initialized")
    stdout.flush()
