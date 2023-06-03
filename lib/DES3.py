from zope.interface import implementer
from .interfaces import IEncryption
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from .RSA import RSA_Wrapper
# from .key_rings import public_key_ring, private_key_ring
from .Msg import Msg

@implementer(IEncryption)
class DES3_Wrapper():
    
    def __init__(self, key):
        self.key = key

    @classmethod
    def generate_session_key(cls):
        while True:
            try:
                key = DES3.adjust_key_parity(get_random_bytes(24))
                break
            except ValueError:
                pass
        return key
    
    def encrypt(self, data):
        if isinstance(data, str):
            data = bytes(data, 'utf-8')
        cipher = DES3.new(self.key, DES3.MODE_CFB)
        ciphertext = cipher.encrypt(data)
        return cipher.iv + ciphertext

    def decrypt(self, data, iv):
        cipher = DES3.new(self.key, DES3.MODE_CFB, iv=iv)
        plaintext = cipher.decrypt(data)
        return plaintext