from time import sleep
from sys import stdout
from sqlalchemy.exc import OperationalError
from pyramda import curry
from .model import UserAuth, create_tables
from .session import with_session
from .create_user import create_user
from .crypto import encrypt


@curry
def with_repeat_on_error(exn_type, num_times, retryable_func):
    for n in range(num_times):
        try:
            return retryable_func(n)
        except exn_type:
            if n == num_times-1:
                raise


def create_tables_with_sleep(num_times_tried):
    print("Attempting database connection...")
    stdout.flush()
    sleep(num_times_tried + 1)
    create_tables()
    print("Succesfully connected, schema initialized")
    stdout.flush()


retry_sqlalchemy_func = with_repeat_on_error(OperationalError, 4)


def initialize_database():
    print("Initializing database")
    retry_sqlalchemy_func(create_tables_with_sleep)
    stdout.flush()
