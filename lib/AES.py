from .interfaces import IEncryption
from zope.interface import implementer
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

@implementer(IEncryption)
class AES_Wrapper():

    def __init__(self, key):
        self.key = key

    @classmethod
    def generate_session_key(cls):
        return get_random_bytes(16)

    def encrypt(self, data):
        data = bytes(data, 'utf-8')
        cipher = AES.new(self.key, AES.MODE_CFB)
        ciphertext = cipher.encrypt(data)
        return ciphertext

    def decrypt(self, data):
        pass