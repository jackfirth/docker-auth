from sqlalchemy.orm import sessionmaker
from engine import engine

Session = sessionmaker(bind=engine)


def with_session(f):
    session = Session()
    try:
        result = f(session)
        session.commit()
        return result
    except:
        session.rollback()
        raise
    finally:
        session.close()
