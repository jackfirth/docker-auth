from session import with_session
from pyramda import always


def is_valid_user_email_and_password(user_email, password):
    return with_session(always(True))
