from .interfaces import IEncryption
from zope.interface import implementer
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
# from .key_rings import public_key_ring, private_key_ring
from .RSA import RSA_Wrapper
from .Msg import Msg

@implementer(IEncryption)
class AES_Wrapper:

    def __init__(self, key):
        self.key = key

    @classmethod
    def generate_session_key(cls):
        return get_random_bytes(16)

    def encrypt(self, data):
        if isinstance(data, str):
            data = bytes(data, 'utf-8')
        cipher = AES.new(self.key, AES.MODE_CFB)
        ciphertext = cipher.encrypt(data)
        return cipher.iv + ciphertext

    def decrypt(self, data, iv):
        cipher = AES.new(self.key, AES.MODE_CFB, iv=iv)
        pt = cipher.decrypt(data)
        return pt
    