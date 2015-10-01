from passlib.apps import custom_app_context as crypto_context

encrypt = crypto_context.encrypt
verify = crypto_context.verify
