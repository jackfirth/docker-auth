from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Column, Integer, String
from config import DB_SCHEMA
from .engine import engine


meta = MetaData(schema=DB_SCHEMA)
Base = declarative_base(metadata=meta)


class UserAuth(Base):
    __tablename__ = 'user_auths'
    id = Column(Integer, primary_key=True)
    email = Column(String(1000), unique=True, nullable=False)
    password = Column(String(1000), nullable=False)


def create_tables():
    Base.metadata.create_all(engine)
