import hashlib

def hash_password(password):
    if isinstance(password, str):
        password = password.encode()
    return hashlib.sha256(password).hexdigest()
    s