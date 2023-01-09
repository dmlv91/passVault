import os
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend
iterations = 100000
salt = os.urandom(16)


def _derive_key(passw: str, salt: bytes = salt, iterations: int = iterations) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=backend
        )
    return kdf.derive(passw.encode())

def pass_encrypt(message: bytes, passw: str, salt: bytes = salt, iterations: int = iterations):
    salt = salt
    key = b64e(_derive_key(passw, salt, iterations))
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )

def pass_decrypt(token: bytes, passw: str) -> bytes:
    decoded = b64d(token)
    salt,iter,token = decoded[:16],decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = b64e(_derive_key(passw,salt, iterations))
    return Fernet(key).decrypt(token)

def generate(passw: str):
    key = _derive_key(passw, salt, iterations)
    return key