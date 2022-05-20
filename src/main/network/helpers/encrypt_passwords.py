import hashlib
import hmac

salt = b'\x9c\x0f\xd7x%\xb2^|\xc5\xe0\xc7\x9f\xcck\x91&c\x16\xaf\xd6\x87\x93\xbe\xe0\x8f<\x0fY\xdev\xe4\xe6'


class encrypt_passwords:

    def __init__(self):
        pass

    def encode(self, password):
        h = hmac.new(salt, password.encode('utf-8'), hashlib.sha1).hexdigest()
        return str(h)

    def compare(self, password, pass_from_db):
        return self.encode(password) == pass_from_db

