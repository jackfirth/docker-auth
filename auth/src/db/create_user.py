from .session import with_session
from .create_model import create_model
from .model import UserAuth
from .crypto import encrypt

create_user_auth = create_model(UserAuth)


def create_user(email, password):
    with_session(create_user_auth({
        "email": email,
        "password": encrypt(password)
    }))
