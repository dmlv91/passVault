import os
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#define internal variables for cryptography functions
iterations = 100000
salt = os.urandom(16)

#Create unique cryptographic key that can be used for password encryption
def _derive_key(passw: str, salt: bytes = salt, iterations: int = iterations) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        )
    return kdf.derive(passw.encode())

#Password encryption function that uses key and master password as parameters
def pass_encrypt(message: bytes, passw: str, salt: bytes = salt, iterations: int = iterations):
    salt = salt
    key = b64e(_derive_key(passw,salt, iterations))
    print(key)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )
#Password decryption function that uses key and master password as parameters
def pass_decrypt(token: bytes, passw: str) -> bytes:
    decoded = b64d(token)
    salt,iter,token = decoded[:16],decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = b64e(_derive_key(passw,salt, iterations))
    print(key)
    return Fernet(key).decrypt(token)

#Function to transfer parameters from outside resources to key derivation function
def generate(passw: str):
    key = _derive_key(passw, salt, iterations)
    return key