from os import environ
from collections import namedtuple
from pyramda import curry


EnvSetting = namedtuple("EnvSetting", "name value")

required_var_msg_format = "No value for required environment variable {0}"
optional_var_msg_format = \
    "No value for optional environment variable {0}, default to {1}"
pred_var_msg_format = \
    "Bad value for environment variable {0}, expected {1}, got {2}"


def required_environ(var):
    var_name = var.name if isinstance(var, EnvSetting) else var
    if var_name not in environ:
        raise EnvironmentError(required_var_message_format % var_name)
    var_value = var.value if isinstance(var, EnvSetting) else environ[var_name]
    return EnvSetting(var_name, var_value)


@curry
def default_environ(default_value, var):
    var_name = var.name if isinstance(var, EnvSetting) else var
    if var_name not in environ:
        print(optional_var_msg_format.format(var_name, default_value))
        return EnvSetting(var_name, default_value)
    var_value = var.value if isinstance(var, EnvSetting) else environ[var_name]
    return EnvSetting(var_name, var_value)


@curry
def pred_environ(pred, coerce_func, description, var):
    var_name = var.name if isinstance(var, EnvSetting) else var
    var_value = var.value if isinstance(var, EnvSetting) else environ[var_name]
    if not pred(var_value):
        raise EnvironmentError(
            pred_var_msg_format.format(var_name, description, var_value)
        )
    return EnvSetting(var_name, coerce_func(var_value))
