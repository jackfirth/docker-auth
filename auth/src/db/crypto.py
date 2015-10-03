from passlib.context import CryptContext
from config import HASH_ROUNDS

crypt_context = CryptContext(
    schemes=["pbkdf2_sha512"],
    all__vary_rounds=0.1,
    pbkdf2_sha512__default_rounds=HASH_ROUNDS
)


encrypt = crypt_context.encrypt
verify = crypt_context.verify
