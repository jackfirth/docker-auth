from pyramda import curry, compose
from .session import with_session
from .model import UserAuth
from .crypto import verify


@curry
def maybe_user_auth(user_email, session):
    return session.query(UserAuth).filter_by(email=user_email).first()


def dump_model(orm_model):
    a_dict = orm_model.__dict__.copy()
    del a_dict["_sa_instance_state"]
    return a_dict


def lift_maybe(f):
    def lifted(v):
        if v is None:
            return None
        else:
            return f(v)
    return lifted


maybe_dump_model = lift_maybe(dump_model)


def is_valid_user_email_and_password(user_email, password):
    maybe_user_auth_data = with_session(compose(
        maybe_dump_model,
        maybe_user_auth(user_email)
    ))
    return maybe_user_auth_data and verify(
        password,
        maybe_user_auth_data["password"]
    )
