from .interfaces import ISignature
from zope.interface import implementer
from Crypto.Signature import DSS
from Crypto.Hash import SHA1
from Crypto.PublicKey import DSA
from Crypto.PublicKey.DSA import DsaKey

@implementer(ISignature)
class DSA_Wrapper():

    def __init__(self, key):
        self.key : DsaKey = key

    @classmethod
    def signature_length(cls, key_length):
        if key_length == 256:
            return 56
        elif key_length == 128:
            return 40
        else:
            return -1
    @classmethod
    def generate_key(cls, key_length):
        return DSA.generate(key_length)

    @classmethod
    def construct_key(cls, y, g, p, q):
        return DSA.construct((y, g, p, q))

    def sign(self, message):
        h = SHA1.new(message)
        dsa = DSS.new(self.key, 'fips-186-3')
        return dsa.sign(h)


    def verify(self, message, signature):
        h = SHA1.new(message)
        dsa = DSS.new(self.key, 'fips-186-3')
        try:
            dsa.verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False