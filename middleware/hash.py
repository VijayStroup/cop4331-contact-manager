from binascii import hexlify
from hashlib import pbkdf2_hmac


def hash_password(password: str, salt: str) -> str:
    """hash plaintext password for strage"""

    hashp = hexlify(pbkdf2_hmac(
        'sha256',
        bytes(password, encoding='utf-8'),
        bytes(salt, encoding='utf-8'),
        100_000
    ))

    return hashp.decode('utf-8')
