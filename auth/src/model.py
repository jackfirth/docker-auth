from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Column, Integer, String
from sqlalchemy.exc import OperationalError
from config import DB_SCHEMA
from time import sleep
from engine import engine
from sys import stdout

meta = MetaData(schema=DB_SCHEMA)
Base = declarative_base(metadata=meta)


class UserAuth(Base):
    __tablename__ = 'user_auths'
    id = Column(Integer, primary_key=True)
    email = Column(String(1000))
    password = Column(String(1000))


def create_tables():
    Base.metadata.create_all(engine)


def with_repeat_on_error(exn_type, num_times, retryable_func):
    for n in range(num_times):
        try:
            return retryable_func(n)
        except exn_type:
            if n == num_times-1:
                raise


def initialize_database():
    print("Initializing database")

    def create_tables_with_sleep(num_times_tried):
        print("Attempting database connection...")
        stdout.flush()
        sleep(num_times_tried + 1)
        create_tables()
        print("Succesfully connected, tables initialized")
        stdout.flush()
    with_repeat_on_error(OperationalError, 4, create_tables_with_sleep)
