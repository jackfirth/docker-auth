from sqlalchemy import create_engine
from config import DB_USER, DB_PASSWORD, DB_HOST


connstring = "postgresql://{0}:{1}@{2}".format(
    DB_USER,
    DB_PASSWORD,
    DB_HOST
)

engine = create_engine(connstring)
