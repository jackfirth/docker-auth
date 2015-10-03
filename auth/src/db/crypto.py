from passlib.context import CryptContext
from config import HASH_ROUNDS, HASH_ALGORITHM

crypt_context = CryptContext(
    schemes=[HASH_ALGORITHM],
    all__vary_rounds=0.1,
    pbkdf2_sha512__default_rounds=HASH_ROUNDS
)


encrypt = crypt_context.encrypt
verify = crypt_context.verify
