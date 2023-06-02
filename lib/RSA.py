from .interfaces import IEncryption
from zope.interface import implementer
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from .Msg import Msg

@implementer(IEncryption)
class RSA_Wrapper():

    def __init__(self, key):
        self.key = key

    @classmethod
    def generate_key(cls, key_size):
        return RSA.generate(key_size)
    
    @classmethod
    def construct_key(cls, n, e):
        return RSA.construct((n, e))

    def encrypt(self, data):
        data = bytes(data, 'utf-8')
        cipher = PKCS1_OAEP.new(self.key)
        ciphertext = cipher.encrypt(data)
        return ciphertext

    def decrypt(self, data):
        cipher = PKCS1_OAEP.new(self.key)
        pt = cipher.decrypt(data)
        return pt
    